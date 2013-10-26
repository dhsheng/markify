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
        customer_id = self.get_argument('customer_id')
        name = self.get_argument('name', '')
        state = self.get_argument('state', 'N')  # default normal states
        session = get_session(scoped=True)
        order_items = []
        try:
            items = json.loads(self.get_argument('items'))
            for item in items:
                length = item['length']
                width = item['width']
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
                    product_id=item['product_id'], product_name=item['product_name'],
                    amount=amount
                )
                order_items.append(order_item)
        except HTTPError:
            pass
        except (KeyError, ValueError):
            pass

        if order_items:
            order = Order(customer_id=customer_id, name=name, state=state)
            product_areas = {}
            for order_item in order_items:
                order_item.order_id = order.id
                if order_item.product_id in product_areas:
                    product_areas[order_item.product_id] += order_item.area
                else:
                    product_areas[order_item.product_id] = order_item.area
            products = session.query(Product).filter(Product.id.in_(
                [binascii.a2b_hex(sid) for sid in product_areas.keys()])).all()
            try:
                for product in products:
                    hid = binascii.b2a_hex(product.id)
                    if hid in product_areas:
                        product.total -= product_areas[hid]
                        session.add(product)
                session.add(order)
                session.add_all(order_items)
                #session.commit()
            except IntegrityError:
                session.rollback()

        return self.finish({'data': json.loads(self.get_argument('items', ''))})


class EditRequestHandler(BaseRequestHandler):

    def post(self):
        pass

    def get(self):
        pass
