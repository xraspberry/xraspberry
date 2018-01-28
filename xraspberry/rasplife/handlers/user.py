import logging

from xraspberry import config
from xraspberry.rasplife.utils import generate_timestamp
from xraspberry.rasplife.handlers.base import route, BaseHandler, user_auth, admin_auth, MESSAGES
from xraspberry.rasplife.models.user import User
from xraspberry.rasplife.db import db_session


@route(r'/user/login')
class UserLoginHandler(BaseHandler):
    def post(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        data = self.get_json_body()
        username = data.get("username")
        password = data.get("password")
        user = User.find_by_name(username)
        if user is None:
            return self.error("Bad username", status_code=403)
        authed = user.check_password(password)
        if not authed:
            return self.error("Bad password", status_code=403)
        self.set_secure_cookie("user_id", str(user.id))
        self.data({})

    def get(self, *args, **kwargs):
        key = self.get_argument("key")
        if key == config.get_config("rasplife.auth_config.secret_key"):
            self.set_secure_cookie("user_id", str(0))
            self.data({})
        else:
            return self.error(MESSAGES[403], status_code=403)


@route(r'/user/logout')
class UserLogoutHandler(BaseHandler):
    @user_auth
    def get(self, *args, **kwargs):
        self.clear_cookie("user_id")
        return self.data({})


@route(r'/user/(\d+)')
class UserInfoHandler(BaseHandler):
    @user_auth
    def get(self, user_id, *args, **kwargs):
        # 普通用户只可以查询管理员信息，不能查询其他用户的信息
        if self.current_user.id != user_id:
            admin_user = db_session.query(User).filter_by(role=User.ADMIN).first()
            if user_id == admin_user.id:
                return self.data(admin_user.to_dict())
            elif self.is_admin():
                query_user = User.find_by_id(user_id)
                if not query_user:
                    return self.error(MESSAGES[404], status_code=404)
                else:
                    return self.data(query_user.to_dict())
        else:
            self.data(self.current_user.to_dict())

    @admin_auth
    def put(self, user_id, *args, **kwargs):
        query_user = User.find_by_id(user_id)
        if not query_user:
            return self.error(MESSAGES[404], status_code=404)
        data = self.get_json_body()
        password = data.pop("password")
        if password:
            query_user.set_password(password)
        try:
            for key, value in data.items():
                if hasattr(query_user, key):
                    setattr(query_user, key, value)
            db_session.add(query_user)
            db_session.commit()
        except Exception as e:
            logging.exception(e)
            return self.error(str(e), status_code=400)
        return self.data(query_user.to_dict())

    @admin_auth
    def delete(self, user_id, *args, **kwargs):
        query_user = User.find_by_id(user_id)
        if not query_user:
            return self.error(MESSAGES[404], status_code=404)
        db_session.query(User).update({User.deleted_at: generate_timestamp()})
        db_session.commit()
        return self.data(query_user.to_dict())


@route(r'/users')
class UsersHandler(BaseHandler):
    @admin_auth
    def get(self, *args, **kwargs):
        users = User.get_users()
        ret = []
        for user in users:
            ret.append(user.to_dict())
        return self.data(ret)


@route(r'/user/register')
class UserRegisterHandler(BaseHandler):
    @admin_auth
    def post(self, *args, **kwargs):
        data = self.get_json_body()
        username = data.get("username")
        password = data.pop("password")
        password2 = data.pop("password2")
        if not (username and password and password2) or password != password2:
            self.error(MESSAGES[400], status_code=400)
        user = User.find_by_name(username)
        if user is not None:
            return self.error("Bad username", status_code=400)
        try:
            new_user = User(**data)
            new_user.set_password(password)
            db_session.add(new_user)
            db_session.commit()
        except Exception as e:
            logging.exception(e)
            return self.error(str(e), status_code=400)
        return self.data(new_user.to_dict())
