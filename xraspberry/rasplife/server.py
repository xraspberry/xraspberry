# -*- coding:utf-8 -*-
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import options

from xraspberry import config
from xraspberry.rasplife.handlers.base import route


class Application(tornado.web.Application):

    def __init__(self):
        logging.info("start rasplife...")

        handlers = route.get_handlers()

        settings = {
            'compiled_template_cache': False,
            'template_path': 'templates',
            'static_path': config.path('xraspberry/rasplife/static'),
            'serve_traceback': True,
            'xsrf_cookies': False,
            "cookie_secret": "rasplifenice",
        }
        tornado.web.Application.__init__(self, handlers, debug=config.get_config("rasplife.debug", True), **settings)


def setup_options():
    # tornado.options是负责解析tornado容器的全局参数的，同时也能够解析命令行传递的参数和从配置文件中解析参数。
    del options._options["logging"]  # reset logging level, pylint: disable=protected-access
    options.define("logging", default=config.get_config("logging.level", default="debug"), help="logging level")
    options.define("port", default=config.get_config("rasplife.http_port"), help="run on the given port ", type=int)
    tornado.options.parse_command_line()


def run():
    setup_options()
    try:
        rasp_app = Application()
        server = tornado.httpserver.HTTPServer(rasp_app)
        server.listen(options.port)
        logging.info("Server started... \nhttp://localhost:%s\n", options.port)
        tornado.ioloop.IOLoop.instance().start()
    except Exception as e:  # pylint: disable=broad-except
        logging.error('catch exception: %s', e)
        raise


if __name__ == "__main__":
    run()
