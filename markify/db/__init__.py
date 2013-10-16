#-*- coding:utf-8 -*-

from markify.config import DB_URL
from markify.config import DEBUG

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import ScopedSession

_GLOBAL_ENGINE = None
_GLOBAL_SESSION = None


def get_engine():
    global _GLOBAL_ENGINE
    if not _GLOBAL_ENGINE:
        _GLOBAL_ENGINE = create_engine(DB_URL, echo=DEBUG)
    return _GLOBAL_ENGINE


def get_session(engine=get_engine(), scoped=False, **kwargs):
    autocommit = kwargs.pop('autocommit', False)
    autoflush = kwargs.pop('autoflush', True)
    if not scoped:
        global _GLOBAL_SESSION
        if not _GLOBAL_SESSION:
            _GLOBAL_SESSION = sessionmaker(bind=engine, autocommit=autocommit, autoflush=autoflush)()
        return _GLOBAL_SESSION
    else:
        return ScopedSession(sessionmaker(bind=engine, autocommit=autocommit, autoflush=autoflush))()

