from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import MetaData
from databases import Database
from starlette.requests import Request


def get_db(request: Request):
    return request.state.db


def get_transaction_id(request: Request):
    return request.state.od_transaction_id


class CustomBase(object):
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=CustomBase, metadata=MetaData())
database = Database('sqlite:////tmp/sqlite.db')
