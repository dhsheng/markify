#-*- coding:utf-8 -*-

import uuid
import time
import json
import binascii

from sqlalchemy.schema import Column
from sqlalchemy.schema import MetaData
from sqlalchemy.types import String
from sqlalchemy.types import Integer
from sqlalchemy.types import LargeBinary
from sqlalchemy.types import Boolean
from sqlalchemy.types import Float
from sqlalchemy.types import Numeric
from sqlalchemy.types import SmallInteger
from sqlalchemy.types import Enum
from sqlalchemy.types import Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.attributes import InstrumentedAttribute

from markify.db import get_engine
from markify.db import get_session


class Model(object):

    pk = Column(Integer, primary_key=True)
    id = Column(LargeBinary(16), unique=True)
    updated = Column(Integer)
    created = Column(Integer)
    deleted = Column(Boolean, default=False)

    _attributes = []

    def __init__(self, **kwargs):
        for key in self.get_attributes():
            if key in kwargs:
                setattr(self, key, kwargs[key])
        if not self.id:
            self.id = binascii.a2b_hex(uuid.uuid4().get_hex())
        if not self.created:
            self.created = int(time.time())
        if not self.updated:
            self.updated = self.created

    def get_attributes(self):
        if not self._attributes:
            self._attributes = [attr for attr in dir(self.__class__)
                                if isinstance(getattr(self.__class__, attr),
                                              InstrumentedAttribute)]
        return self._attributes

    def is_valid(self):
        return True

    def get_errors(self):
        return {}

    def safe_convert(self, typ, val):
        if isinstance(typ, LargeBinary):
            return binascii.b2a_hex(val)
        elif isinstance(typ, Numeric):
            return round(val, 2)
        return val

    def to_dict(self):
        data = {}
        for col in self._sa_class_manager.mapper.mapped_table.columns:
            typ, name = col.type, col.name
            data[name] = self.safe_convert(typ, getattr(self, name))
        return data

    def to_json(self):
        return json.dumps(self.to_dict())



Base = declarative_base(bind=get_engine(), metadata=MetaData())


class User(Model, Base):

    __tablename__ = 'users'

    email = Column(String(150), nullable=False, unique=True)
    username = Column(String(30), nullable=False, unique=True)
    password = Column(String(32), nullable=False)
    is_active = Column(Boolean, default=True)
    last_login_at = Column(Integer, default=0)
    login_count = Column(SmallInteger, default=0)

    def __repr__(self):
        return self.username or self.email


class Customer(Model, Base):

    __tablename__ = 'customers'

    user_id = Column(LargeBinary(16), nullable=False)
    email = Column(String(150), nullable=False, default='')
    name = Column(String(50), nullable=False, default='')
    phone = Column(String(14), nullable=False, default='')
    addition_phone = Column(String(14), nullable=False, default='')
    address = Column(String(255), nullable=False, default='')

    def __repr__(self):
        return self.name


class Product(Model, Base):

    __tablename__ = 'products'
    user_id = Column(LargeBinary(16), nullable=False)
    name = Column(String(255), nullable=False)
    stock = Column(Float, nullable=False, default=.00)
    amount = Column(Numeric, nullable=False, default=.00)
    unit = Column(String(20), nullable=False, default='')

    def __repr__(self):
        return self.name


class Order(Model, Base):

    FAILED = 'F'
    SUCCESS = 'S'
    NORMAL = 'N'

    __tablename__ = 'orders'
    customer_id = Column(LargeBinary(16), nullable=False)
    customer_name = Column(String(50), nullable=False)
    name = Column(String(150), nullable=False)
    state = Column(Enum(*(FAILED, SUCCESS, NORMAL), name='order_state'))
    modified_logs = Column(Text)
    amount = Column(Numeric, nullable=False, default=.00)

    def get_items(self):
        session = get_session()
        order_items = session.query(OrderItem).filter(
            OrderItem.order_id == self.id).all()
        for order_item in order_items:
            yield order_item
        session.close()

    def items_to_json(self, id_as_key=False):
        items = {} if id_as_key else []
        for item in self.get_items():
            if id_as_key:
                item = item.to_dict()
                items[item.pop('id')] = item
            else:
                items.append(item.to_dict())
        return json.dumps(items)

    def to_json(self):
        data = self.to_dict()
        data['items'] = [item.to_dict() for item in self.get_items()]
        return json.dumps(data)




class OrderItem(Model, Base):

    __tablename__ = 'order_items'
    CHAMFER_SIZE = 4

    order_id = Column(LargeBinary(16))
    product_id = Column(LargeBinary(16))
    product_name = Column(String(255))
    length = Column(Float)
    width = Column(Float)
    count = Column(Integer)
    price = Column(Numeric)
    area = Column(Float)
    steel_price = Column(Numeric, default=.00)
    steel_count = Column(Float, default=0)
    drill_price = Column(Numeric, default=.00)
    drill_count = Column(Float, default=0)
    paint_price = Column(Numeric, default=.00)
    paint_count = Column(Float, default=0)
    edg_price = Column(Numeric, default=.00)
    edg_count = Column(Numeric, default=0)
    chamfer_price = Column(Numeric, default=.00)
    chamfer_count = Column(Float, default=.0)
    amount = Column(Numeric, default=.0)

    def __repr__(self):
        return u'%s[%sx%s]' % (self.product_id, self.length, self.width)


class OrderAdditionFee(Model, Base):
    __tablename__ = 'order_addition_fees'


class PriceHistory(Model, Base):

    __tablename__ = 'price_histories'

    order_item_id = Column(LargeBinary(16))
    order_id = Column(LargeBinary(16))
    price = Column(Numeric)
    price_type = Column(String(100))

    def __repr__(self):
        return self.price
