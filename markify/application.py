#-*- coding:utf-8 -*-

from tornado.ioloop import IOLoop
from tornado.web import url
from tornado.web import Application as BaseApplication

import config

from markify.handlers import user
from markify.handlers import order
from markify.handlers import product


class Application(BaseApplication):

    def __init__(self):
        handlers = [
            url(r'/order/create', order.CreateRequestHandler, name='order.create'),
            url(r'/product/create', product.CreateRequestHandler, name='product.create'),
            url(r'/products', product.ListRequestHandler, name='products'),
            url(config.LOGIN_URL, user.LoginRequestHandler, name='login'),
            url(r'/register', user.RegisterRequestHandler, name='register'),
            url(r'/logout', user.LogoutRequestHandler, name='logout'),
        ]
        settings = {
            'Debug': config.DEBUG,
            'cookie_secret': config.SESSION_KEY,
            'template_path': config.TEMPLATE_DIRS,
            'login_url': config.LOGIN_URL,
            'xsrf_cookies': config.ENABLE_XSRF_TOKEN,
            'static_path': config.STATIC_PATH
        }
        super(Application, self).__init__(handlers, **settings)


if __name__ == '__main__':
    if config.DEBUG:
        from markify.db.models import Base
        Base.metadata.create_all()
    application = Application()
    application.listen(8888)
    IOLoop.instance().start()
