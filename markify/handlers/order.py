#-*- coding:utf-8 -*-

import binascii

from tornado.web import HTTPError
from tornado.web import authenticated

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

from markify.config import RESPONSE_ERROR_KEY
from markify.config import RESPONSE_DATA_KEY
from markify.config import RESPONSE_FLAG_KEY
from markify.db import get_session
from markify.db.models import Order
from markify.db.models import OrderAdditionFee
from markify.db.models import OrderItem
from markify.db.models import Product
from markify.db.models import Customer


from markify.handlers.base import BaseRequestHandler


class CreateRequestHandler(BaseRequestHandler):

    def get(self):
        return self.render('order/create.mako')

    def post(self):
        user_id = self.get_current_user()
        customer_id = self.get_argument('customer_id', '')
        name = self.get_argument('name', '')
        state = self.get_argument('state', 'N')  # default normal states
        session = get_session(scoped=True)
        order = Order(name=name, state=state, user_id=binascii.a2b_hex(user_id),
                      customer_id=binascii.a2b_hex(customer_id))
        try:
            order_items = []
            session.add(order)
            session.add(order_items)
            session.commit()
        except IntegrityError:
            session.rollback()
        finally:
            if session:
                session.close()


class EditRequestHandler(BaseRequestHandler):

    def post(self):
        pass

    def get(self):
        pass
