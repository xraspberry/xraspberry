# encoding: utf8
import logging
import functools
import importlib
import json

import psycopg2
import sqlalchemy.exc
import tornado.web

from xraspberry.rasplife.db import db_session
from xraspberry.rasplife.models.user import User


MESSAGES = {
    400: "Bad Request",
    403: "Forbidden",
    404: "Not Found"
}


class route(object):  # pylint: disable=invalid-name
    HANDLERS = []

    def __init__(self, router_url, prefix="/api/v1"):
        self.router_url = router_url
        self.prefix = prefix

    def __call__(self, clz):
        url = "{}{}".format(self.prefix, self.router_url)
        self.__class__.HANDLERS.append((url, clz))
        return clz

    @classmethod
    def get_handlers(cls):
        handlers = ["user"]
        for handler in handlers:
            importlib.import_module("xraspberry.rasplife.handlers.{}".format(handler))
        return cls.HANDLERS


class UserAuth(object):
    def __init__(self, group):
        self.group = group

    def auth_check(self, this):
        if this.current_user is None:
            return False
        else:
            flag = True
            if self.group == "user":
                pass
            elif self.group == "current":
                if not this.is_admin():
                    flag = False
            elif self.group == "admin":
                if not this.is_admin():
                    flag = False
            else:
                flag = False
            return flag

    def __call__(self, method):
        @functools.wraps(method)
        def wrapper(this, *args, **kwargs):
            if not self.auth_check(this):
                raise tornado.web.HTTPError(403)
            return method(this, *args, **kwargs)

        return wrapper


user_auth = UserAuth("user")
current_auth = UserAuth("current")
admin_auth = UserAuth("admin")


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.user_data = None

    def data_received(self, chunk):
        pass

    def log_exception(self, typ, value, tb):
        if isinstance(value, (psycopg2.DatabaseError, sqlalchemy.exc.SQLAlchemyError)):
            db_session.rollback()
        super(BaseHandler, self).log_exception(typ, value, tb)

    def get_current_user(self):
        uid_in_cookie = self.get_secure_cookie("user_id")
        if uid_in_cookie is None:
            return
        uid = int(uid_in_cookie)
        if uid > 0:
            self.user_data = User.find_by_id(uid)
        else:
            self.user_data = User(id=0, username="dummy", role=User.ADMIN)
        return self.user_data

    def get_json_body(self):
        """Return the body of the request as JSON data."""
        if not self.request.body:
            return None
        body = self.request.body
        try:
            model = json.loads(body.strip().decode(u'utf-8'))
        except Exception:
            logging.debug("Bad DATA FORMAT: %r", body)
            logging.error("Couldn't parse DATA", exc_info=True)
            raise tornado.web.HTTPError(400, u'Invalid DATA in body of request')
        return model

    def is_current(self):
        return self.current_user.role == User.CURRENT

    def is_admin(self):
        return self.current_user.role == User.ADMIN

    def send_json(self, data):
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(data))

    def data(self, data):
        self.send_json({"status": "ok", "data": data})

    def error(self, message, status_code=200, binary=None):
        self.set_status(status_code)
        self.send_json({"status": "error", "message": message})

    def on_finish(self):
        db_session.commit()
