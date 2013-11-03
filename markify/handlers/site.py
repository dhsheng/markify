#-*- coding:utf-8 -*-

from markify.handlers.base import BaseRequestHandler


class ErrorRequestHandler(BaseRequestHandler):

    def get(self):
        return self.render('error.mako')