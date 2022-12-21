from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()


class DBSession:
    def __init__(self, module):
        _db_uri = "mysql://root:secret@mariadb-service/notebook?charset=utf8mb4"
        _echo = True
        # engine = create_engine(_db_uri, echo=_echo, poolclass=NullPool)
        engine = create_engine(_db_uri, echo=_echo)
        session = scoped_session(sessionmaker(bind=engine))
        if session is None:
            print("Failed to connect to Database!")

        self.engine = engine
        self.session = session

        if module:
            self.session.module = module
            self.session.module.metadata.create_all(engine)

    def close(self):
        if self.session is not None:
            self.session.remove()
            self.engine.dispose()
