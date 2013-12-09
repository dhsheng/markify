#-*- coding:utf-8 -*-

from mako.lookup import TemplateLookup
from tornado.web import RequestHandler
from markify.config import SESSION_KEY


class BaseRequestHandler(RequestHandler):

    def get_current_user(self):
        user_id = self.get_cookie(SESSION_KEY, '')
        return user_id

    def render_string(self, template_name, **kwargs):
        dirs = list(self.application.settings['template_path'])
        lookup = TemplateLookup(dirs, input_encoding='utf-8', output_encoding='utf-8')
        kwargs['request'] = self
        return lookup.get_template(template_name).render(**kwargs)

