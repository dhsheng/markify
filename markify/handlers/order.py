#-*- coding:utf-8 -*-

from markify.handlers.base import BaseRequestHandler


class CreateRequestHandler(BaseRequestHandler):

    def get(self):
        return self.render('order/create.mako')

    def post(self):
        pass


class EditRequestHandler(BaseRequestHandler):

    def post(self):
        pass

    def get(self):
        pass

