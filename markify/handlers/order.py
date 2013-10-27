#-*- coding:utf-8 -*-

import binascii
import json

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
        user_id = user_id or '7a5e2622155442d7b1f2e623b7bc87bb'
        customer_id = self.get_argument('customer_id', user_id)
        name = self.get_argument('name', '')
        customer_name = self.get_argument('customer_name', '')
        state = self.get_argument('state', 'N')  # default normal states
        session = get_session(scoped=True)
        order_items = []
        try:
            items = json.loads(self.get_argument('items'))
            for item in items:
                length = float(item['length'])
                width = float(item['width'])
                area = (length / 1000.0) * (width / 1000.0)
                drill_price = float(item['drill_price'])
                steel_price = float(item['steel_price'])
                edg_price = float(item['edg_price'])
                chamfer_price = float(item['chamfer_price'])
                paint_price = float(item['paint_price'])
                price = float(item['price'])
                count = float(item['count'])
                amount_chamfer = chamfer_price * (item.get('chamfer_count', 0)
                                                  or (count * OrderItem.CHAMFER_SIZE))
                total_area = area * count
                amount_drill = drill_price * (item.get('drill_count', 0) or total_area)
                amount_paint = paint_price * (item.get('paint_count', 0) or total_area)
                amount_edg = edg_price * (item.get('edg_count', 0) or total_area)
                amount_steel = steel_price * (item.get('steel_count', 0) or total_area)
                amount = (amount_chamfer + amount_paint + amount_drill + amount_steel + amount_edg)
                amount += (price * total_area)
                order_item = OrderItem(
                    length=length, width=width, area=total_area, price=price,
                    count=count, chamfer_price=chamfer_price,
                    chamfer_count=(item.get('chamfer_count', 0) or (count * OrderItem.CHAMFER_SIZE)),
                    paint_price=paint_price, paint_count=(item.get('paint_count', 0) or total_area),
                    drill_price=drill_price, drill_count=(item.get('drill_count', 0) or total_area),
                    edg_price=edg_price, edg_count=(item.get('edg_count', 0) or total_area),
                    steel_price=steel_price, steel_count=(item.get('steel_count', 0) or total_area),
                    product_id=binascii.a2b_hex(item['product_id']), product_name=item['product_name'],
                    amount=amount
                )
                order_items.append(order_item)
        except HTTPError:
            pass
        except (KeyError, ValueError) as e:
            print '*' * 20, e.message

        if order_items:
            order = Order(customer_id=binascii.a2b_hex(customer_id),
                          customer_name=customer_name,
                          amount=sum([item.amount for item in order_items]),
                          name=name, state=state, user_id=user_id)
            product_areas = {}
            for order_item in order_items:
                order_item.order_id = order.id
                print order_item.area
                if order_item.product_id in product_areas:
                    product_areas[order_item.product_id] += order_item.area
                else:
                    product_areas[order_item.product_id] = order_item.area

            products = session.query(Product).filter(Product.id.in_(
                product_areas.keys())).all()
            try:
                for product in products:
                    if product.id in product_areas:
                        print product_areas[product.id], ' sub'
                        product.stock = product.stock - product_areas[product.id]
                        session.add(product)
                session.add(order)
                session.add_all(order_items)
                session.commit()
            except IntegrityError:
                session.rollback()

        return self.finish({'data': json.loads(self.get_argument('items', ''))})


class EditRequestHandler(BaseRequestHandler):

    def post(self):
        pass

    def get(self):
        order_id = self.get_argument('id')
        user_id = self.get_current_user()
        s = get_session()
        order = s.query(Order).filter(Order.id == binascii.a2b_hex(order_id)).one()

        return self.render('order/edit.mako', **{'order': order})


class ListRequestHandler(BaseRequestHandler):

    def get(self):
        s = get_session(scoped=True)
        orders = s.query(Order).all()
        return self.render('order/list.mako', **{'orders': orders})