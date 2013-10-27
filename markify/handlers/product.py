#-*- coding:utf-8 -*-

import binascii

from tornado.web import HTTPError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from markify.config import RESPONSE_DATA_KEY
from markify.config import RESPONSE_FLAG_KEY
from markify.config import RESPONSE_ERROR_KEY
from markify.db import get_session
from markify.db.models import Product
from markify.db.models import User
from markify.handlers.base import BaseRequestHandler


class CreateRequestHandler(BaseRequestHandler):

    def get(self):
        pass

    def post(self):
        name = self.get_argument('name', '')
        stock = self.get_argument('stock', '')
        amount = self.get_argument('amount', '')
        unit = self.get_argument('unit', '')
        user_id = self.get_current_user() or '7a5e2622155442d7b1f2e623b7bc87bb'
        product = Product(name=name, total=stock,
                          user_id=binascii.a2b_hex(user_id),
                          amount=amount, unit=unit)
        data = {}
        if product.is_valid():
            session = get_session(scoped=True)
            try:
                session.add(product)
                session.commit()
                data[RESPONSE_FLAG_KEY] = True
            except IntegrityError as e:
                print e
                session.rollback()
                data[RESPONSE_FLAG_KEY] = False
        else:
            data[RESPONSE_FLAG_KEY] = False
            data[RESPONSE_DATA_KEY] = product.get_errors()
        return self.finish(data)


class ListRequestHandler(BaseRequestHandler):

    def get(self):
        session = get_session(scoped=True)
        user_id = '7a5e2622155442d7b1f2e623b7bc87bb'
        products = session.query(Product).filter_by(user_id=binascii.a2b_hex(user_id)).all()
        return self.render('product/list.mako', **{'products': products})


class EditRequestHandler(BaseRequestHandler):

    def get(self):
        pass

    def post(self):
        session = get_session(scoped=True)
        try:
            product = session.query(Product).filter(id=binascii.a2b_hex(
                self.get_argument('id')
            )).one()
            product.name = self.get_argument('name')
            product.amount = self.get_argument('amount')
            product.stock = self.get_argument('stock')
            session.add(product)
            session.commit()
        except (TypeError, HTTPError):
            pass
        except (NoResultFound, MultipleResultsFound):
            pass
        except IntegrityError:
            session.rollback()
        if session:
            session.close()


class DeleteRequestHandler(BaseRequestHandler):

    def check_xsrf_cookie(self):
        pass

    #@authenticated
    def post(self):
        id = self.get_argument('id', '')
        user_id = self.get_current_user() or '7a5e2622155442d7b1f2e623b7bc87bb'
        session = get_session(scoped=True)
        data = {}
        try:
            customer = session.query(Product).filter(
                Product.id == binascii.a2b_hex(id),
                Product.user_id == binascii.a2b_hex(user_id)).one()
            session.delete(customer)
            session.commit()
            data[RESPONSE_FLAG_KEY] = True
        except (NoResultFound, MultipleResultsFound):
            data[RESPONSE_FLAG_KEY] = False
        finally:
            if session:
                session.close()
        return self.finish(data)