#-*- coding:utf-8 -*-

from tornado.ioloop import IOLoop
from tornado.web import url
from tornado.web import Application as BaseApplication

import config

from markify.handlers import user
from markify.handlers import order
from markify.handlers import product
from markify.handlers import customer
from markify.handlers import site


class Application(BaseApplication):

    def __init__(self):
        handlers = [
            url(r'/order/create', order.CreateRequestHandler, name='order.create'),
            url(r'/order/edit', order.EditRequestHandler, name='order.edit'),
            url(r'^/$', order.ListRequestHandler, name='orders'),
            url(r'/product/create', product.CreateRequestHandler, name='product.create'),
            url(r'/products', product.ListRequestHandler, name='products'),
            url(r'/product/edit', product.EditRequestHandler, name='product.edit'),
            url(r'/product/delete', product.DeleteRequestHandler, name='product.delete'),
            url(config.LOGIN_URL, user.LoginRequestHandler, name='login'),
            url(r'/customers', customer.ListRequestHandler, name='customers'),
            url(r'/customer/create', customer.CreateRequestHandler, name='customer.create'),
            url(r'/customer/edit', customer.EditRequestHandler, name='customer.edit'),
            url(r'/customer/delete', customer.DeleteRequestHandler, name='customer.delete'),
            url(r'/customer/view', customer.ViewRequestHandler, name='customer.view'),
            url(r'/register', user.RegisterRequestHandler, name='register'),
            url(r'/logout', user.LogoutRequestHandler, name='logout'),
            url(r'/error', site.ErrorRequestHandler, name='error')
        ]

        settings = {
            'debug': config.DEBUG,
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
