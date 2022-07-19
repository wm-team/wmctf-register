from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base


class DB:
    Base = declarative_base()

    def __init__(self, uri: str):
        self.engine = create_engine(uri)
        self.Base.metadata.bind = self.engine
        self.session: orm.Session = orm.scoped_session(
            orm.sessionmaker())(bind=self.engine)
        self.Base.metadata.create_all()
