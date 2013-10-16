#-*- coding:utf-8 -*-

import os
import sys

DEBUG = True

BASE_DIRECTORY = os.path.join(os.path.realpath(os.path.dirname(os.getcwd())))

sys.path.insert(0, BASE_DIRECTORY)

DB_URL = 'postgresql://markify:#!python@localhost/'

SESSION_KEY = '0a9458dea/dkal327d&##!dkslab3a0ff9ac2cb8e0473f'

LOGIN_URL = '/login'
ENABLE_XSRF_TOKEN = True
LOGGED_REDIRECT_URL = '/dashboard'

RESPONSE_DATA_KEY = 'data'
RESPONSE_FLAG_KEY = 'success'
RESPONSE_ERROR_KEY = 'error'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIRECTORY, 'templates'),
)

UPLOAD_MEDIA_DIR = '/srv/markify.me/media'
MEDIA_HOST = 'http://media.distreet.com/'

