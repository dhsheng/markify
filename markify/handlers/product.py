#-*- coding:utf-8 -*-

import binascii

from tornado.web import HTTPError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from markify.config import RESPONSE_DATA_KEY
from markify.config import RESPONSE_FLAG_KEY
from markify.db import get_session
from markify.db.models import Product
from markify.handlers.base import BaseRequestHandler


class CreateRequestHandler(BaseRequestHandler):

    def get(self):
        pass

    def post(self):
        name = self.get_argument('name', '')
        stock = self.get_argument('stock', '')
        amount = self.get_argument('amount', '')
        unit = self.get_argument('unit', '')
        user_id = self.get_current_user()
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
            except IntegrityError:
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
        if self.get_argument('format', '') == 'json':
            return self.finish({RESPONSE_FLAG_KEY: True, RESPONSE_DATA_KEY: [
                {'name': p.name, 'id': binascii.b2a_hex(p.id)} for p in products
            ]})
        return self.render('product/list.mako', **{'products': products})


class EditRequestHandler(BaseRequestHandler):

    def get(self):
        id = self.get_argument('id', '')
        user_id = self.get_current_user()
        session = get_session(scoped=True)
        error = False
        try:
            product = session.query(Product).filter(
                Product.id == binascii.a2b_hex(id),
                Product.user_id == binascii.a2b_hex(user_id)).one()
        except (NoResultFound, MultipleResultsFound, TypeError):
            error = True
        finally:
            if session:
                session.close()
        if error:
            return self.render('error.mako')
        return self.render('product/edit.mako', **{'product': product})

    def post(self):
        session = get_session()
        error = False
        try:
            product = session.query(Product).filter(Product.id == binascii.a2b_hex(
                self.get_argument('id')
            ), Product.user_id == binascii.a2b_hex(self.get_current_user())).one()
            product.name = self.get_argument('name')
            product.amount = round(float(self.get_argument('amount')), 2)
            product.stock = round(float(self.get_argument('stock')), 2)
            product.unit = self.get_argument('unit')
            session.add(product)
            session.commit()
        except (TypeError, HTTPError, NoResultFound, MultipleResultsFound):
            error = True
        except IntegrityError:
            session.rollback()
            error = True
        if session:
            session.close()
        if error:
            return self.render('error.mako')
        return self.redirect(self.reverse_url('products'))


class DeleteRequestHandler(BaseRequestHandler):

    def check_xsrf_cookie(self):
        pass

    #@authenticated
    def post(self):
        id = self.get_argument('id', '')
        user_id = self.get_current_user()
        session = get_session(scoped=True)
        data = {}
        try:
            product = session.query(Product).filter(
                Product.id == binascii.a2b_hex(id),
                Product.user_id == binascii.a2b_hex(user_id)).one()
            session.delete(product)
            session.commit()
            data[RESPONSE_FLAG_KEY] = True
        except (NoResultFound, MultipleResultsFound):
            data[RESPONSE_FLAG_KEY] = False
        finally:
            if session:
                session.close()
        return self.finish(data)