import logging

from xraspberry import config
from xraspberry.rasplife.utils import generate_timestamp
from xraspberry.rasplife.handlers.base import route, BaseHandler, user_auth,\
    admin_auth, MESSAGES, user_visit_auth, current_auth
from xraspberry.rasplife.models import User, Post, Todo
from xraspberry.rasplife.db import db_session


@route(r'/user/login')
class UserLoginHandler(BaseHandler):
    def post(self, *args, **kwargs):
        data = self.get_json_body()
        username = data.get("username")
        password = data.get("password")
        user = User.find_by_name(username)
        if user is None or user.deleted_at != 0:
            return self.error("Bad username", status_code=403)
        authed = user.check_password(password)
        if not authed:
            return self.error("Bad password", status_code=403)
        self.set_secure_cookie("user_id", str(user.id), httponly=True)
        self.data({})

    def get(self, *args, **kwargs):
        key = self.get_argument("key")
        if key == config.get_config("rasplife.auth_config.secret_key"):
            self.set_secure_cookie("user_id", str(0), httponly=True)
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
    @user_visit_auth
    @current_auth
    def get(self, user_id, *args, **kwargs):
        if user_id == self.current_user.id:
            return self.data(self.current_user.to_dict())
        query_user = User.find_by_id(user_id)
        if not query_user:
            return self.error(MESSAGES[404], status_code=404)
        else:
            return self.data(query_user.to_dict())

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
        """
        TODO 删除一个用户需要删除其 posts, todos, todo_items
        TODO 都是软删除，即将deleted_at置为当前时间戳
        :param user_id:
        :param args:
        :param kwargs:
        :return:
        """
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


@route(r'/user/(\d+)/posts')
class UserPostsHandler(BaseHandler):
    """
    获取某个用户下的博文列表，可以将user_id作为/posts接口的查询参数
    但是为了更好的权限控制：普通用户不能查看已经删除用户的博文列表
    所以单独做一个接口
    """
    @user_visit_auth
    @current_auth
    def get(self, user_id, *args, **kwargs):
        try:
            page = int(self.get_argument("page", 1))
            size = int(self.get_argument("size", 20))
        except ValueError as e:
            self.error(MESSAGES[400], status_code=400)

        offset = (page - 1) * size
        total, items = Post.get_posts_by_user(user_id, limit=size, offset=offset, is_admin=self.is_admin())

        ret = {
            "total": total,
            "items": [item.to_dict() for item in items],
            "page": page,
            "size": size
        }

        self.data(ret)


@route(r'/user/(\d+)/todos')
class UserTodosHandler(BaseHandler):
    @user_visit_auth
    @current_auth
    def get(self, user_id, *args, **kwargs):
        try:
            page = int(self.get_argument("page", 1))
            size = int(self.get_argument("size", 20))
        except ValueError as e:
            self.error(MESSAGES[400], status_code=400)

        offset = (page - 1) * size
        total, items = Todo.get_todo_by_user(user_id, limit=size, offset=offset, is_admin=self.is_admin())

        ret = {
            "total": total,
            "items": items,
            "page": page,
            "size": size
        }

        self.data(ret)
