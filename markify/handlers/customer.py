#-*- coding:utf-8 -*-

import binascii

from tornado.web import authenticated
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

from markify.config import RESPONSE_DATA_KEY
from markify.config import RESPONSE_ERROR_KEY
from markify.config import RESPONSE_FLAG_KEY
from markify.db import get_session
from markify.db.models import Customer
from markify.handlers.base import BaseRequestHandler


class CustomerRequestHandler(BaseRequestHandler):

    def extract_params(self):
        name = self.get_argument('name', '')
        phone = self.get_argument('phone', '')
        addition_phone = self.get_argument('addition_phone', '')
        address = self.get_argument('address', '')
        email = self.get_argument('email', '')
        return name, phone, addition_phone, address, email


class ListRequestHandler(CustomerRequestHandler):

    def get(self):
        session = get_session(scoped=True)
        customers = session.query(Customer).all()
        return self.render('customer/list.mako', **{'customers': customers})


class CreateRequestHandler(CustomerRequestHandler):

    def get(self):
        return self.render('customer/create.mako')

    #@authenticated
    def post(self):
        name, phone, addition_phone, address, email = self.extract_params()
        user_id = self.get_current_user() or '7a5e2622155442d7b1f2e623b7bc87bb'
        customer = Customer(
            name=name, phone=phone, address=address,
            addition_phone=addition_phone, email=email,
            user_id=binascii.a2b_hex(user_id)
        )
        data = {}
        if customer.is_valid():
            session = get_session(scoped=True)
            try:
                session.add(customer)
                session.commit()
            except IntegrityError as e:
                session.rollback()
                data[RESPONSE_DATA_KEY] = e.message
            finally:
                if session:
                    session.close()
        else:
            data[RESPONSE_ERROR_KEY] = customer.get_errors()
        if RESPONSE_ERROR_KEY in data:
            data[RESPONSE_FLAG_KEY] = False
        else:
            data[RESPONSE_FLAG_KEY] = True
        return self.finish(data)


class EditRequestHandler(CustomerRequestHandler):

    def get(self):
        pass

    @authenticated
    def post(self):
        id = self.get_argument('id', '')
        user_id = self.get_current_user()
        session = get_session(scoped=True)
        try:
            customer = session.query(Customer).filter(id=binascii.a2b_hex(id),
                                                      user_id=binascii.a2b_hex(user_id)).one()
        except(NoResultFound, MultipleResultsFound) as e:
            data = {RESPONSE_FLAG_KEY: False, RESPONSE_ERROR_KEY: e.message}
            return self.finish(data)
        name, phone, addition_phone, address, email = self.extract_params()
        customer.name = name
        customer.phone = phone
        customer.email = email
        customer.addition_phone = addition_phone
        customer.address = address
        data = {}
        try:
            session.add(customer)
            session.commit()
            data[RESPONSE_FLAG_KEY] = True
            data[RESPONSE_DATA_KEY] = customer.to_dict()
        except IntegrityError as e:
            session.rollback()
            data[RESPONSE_DATA_KEY] = e.message
            data[RESPONSE_FLAG_KEY] = False
        finally:
            if session:
                session.close()
        return self.finish(data)


class DeleteRequestHandler(CustomerRequestHandler):

    def check_xsrf_cookie(self):
        pass

    #@authenticated
    def post(self):
        id = self.get_argument('id', '')
        user_id = self.get_current_user() or '7a5e2622155442d7b1f2e623b7bc87bb'
        session = get_session(scoped=True)
        data = {}
        try:
            customer = session.query(Customer).filter(
                Customer.id == binascii.a2b_hex(id),
                Customer.user_id == binascii.a2b_hex(user_id)).one()
            session.delete(customer)
            session.commit()
            data[RESPONSE_FLAG_KEY] = True
        except (NoResultFound, MultipleResultsFound):
            data[RESPONSE_FLAG_KEY] = False
        finally:
            if session:
                session.close()
        return self.finish(data)


class ViewRequestHandler(CustomerRequestHandler):

    @authenticated
    def get(self):
        id = self.get_argument('id', '')
        user_id = self.get_current_user()
        session = get_session(scoped=True)
        data = {}
        try:
            customer = session.query(Customer).filter(
                id=binascii.a2b_hex(id),
                user_id=binascii.a2b_hex(user_id)).one()
            data[RESPONSE_DATA_KEY] = customer.to_dict()
            data[RESPONSE_FLAG_KEY] = True
        except (NoResultFound, MultipleResultsFound):
            data[RESPONSE_FLAG_KEY] = False
        finally:
            if session:
                session.commit()
        return self.finish(data)
