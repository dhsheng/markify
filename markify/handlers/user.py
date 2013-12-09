#-*- coding:utf-8 -*-

from hashlib import md5
from binascii import b2a_hex

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

from markify.config import SESSION_KEY
from markify.config import LOGIN_URL
from markify.config import RESPONSE_DATA_KEY
from markify.config import RESPONSE_ERROR_KEY
from markify.config import RESPONSE_FLAG_KEY
from markify.config import LOGGED_REDIRECT_URL
from markify.db import get_session
from markify.db.models import User
from markify.handlers.base import BaseRequestHandler


class RegisterRequestHandler(BaseRequestHandler):

    def post(self):
        email = self.get_argument('email', '')
        password = self.get_argument('password', '')
        username = self.get_argument('username', '')
        user = User(username=username,
                    password=md5(password).hexdigest(),
                    email=email)
        session = get_session(scoped=True)
        data = {}
        try:
            session.add(user)
            session.commit()
            data[RESPONSE_DATA_KEY] = user.to_dict()
            data[RESPONSE_FLAG_KEY] = True
        except IntegrityError:
            data[RESPONSE_ERROR_KEY] = u'an error occurred'
            data[RESPONSE_DATA_KEY] = False
        finally:
            if session:
                session.close()
        return self.finish(data)

    def get(self):
        return self.render('user/register.html')


class LoginRequestHandler(BaseRequestHandler):

    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        redirect = self.get_argument('next', LOGGED_REDIRECT_URL)
        session = get_session(scoped=True)
        try:
            user = session.query(User).filter(User.username == username).one()
            if password and user.password == md5(password).hexdigest():
                self.set_cookie(SESSION_KEY, b2a_hex(user.id))
                self.set_cookie('username', user.username)
                return self.redirect(redirect)
            raise NoResultFound('login failed')
        except NoResultFound:
            raise NoResultFound
        except MultipleResultsFound:
            raise MultipleResultsFound

    def get(self):
        return self.render('user/login.html')


class LogoutRequestHandler(BaseRequestHandler):

    def get(self):
        self.clear_cookie(SESSION_KEY)
        return self.redirect(LOGIN_URL)
