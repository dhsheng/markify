#-*- coding:utf-8 -*-

from sqlalchemy import func
from markify.db import get_session
from markify.db.models import PriceHistory


def get_frequently_price(typ, session=None, limit=None):
    if not session:
        session = get_session(scoped=True)
    query = session.query(PriceHistory.price, func.count(PriceHistory.price)).group_by(
        PriceHistory.price).filter(PriceHistory.price_type == typ)
    if limit:
        query = query.limit(limit)
    return [{'c': int(pair[0]), 'p': float(pair[1])} for pair in query.all()]
