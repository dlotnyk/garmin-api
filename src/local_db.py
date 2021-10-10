import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from typing import List, Tuple

from logger import log_settings
from table_scheme import MainTable, main_table_name, Base

app_log = log_settings()
local_db_name = "common.db"


class LocalDb:
    """
    local db based of sqlite3
    """
    _table_name = main_table_name

    def __init__(self, db_name: str) -> None:
        try:
            self.db_name = db_name
            self._session = None
            cur_path = os.path.dirname(os.getcwd())
            db_path = os.path.join(cur_path, db_name)
            connector = "sqlite:///" + db_path
            self._db_engine = db.create_engine(connector)
            app_log.debug(f"Engine creates for {db_name}")
        except Exception as ex:
            app_log.error(f"Can not create an engine: `{ex}`")

    @property
    def db_engine(self):
        return self._db_engine

    def create_main_table(self):
        metadata = db.MetaData()
        self.main_tb = db.Table(self._table_name, metadata,
                                db.Column("id", db.Integer, primary_key=True, autoincrement=True),
                                db.Column("name", db.String),
                                db.Column("surname", db.String)
                                )
        try:
            Base.metadata.create_all(self.db_engine)
            app_log.debug(f"Table `{self._table_name}` was created")
        except Exception as ex:
            app_log.error(f"Can not create table: `{ex}`")

    def open_session(self):
        """
        Opens the local db
        """
        try:
            sess = sessionmaker(bind=self.db_engine)
            self._session = sess()
            app_log.debug(f"Session creates for: `{self.db_name}` ")
        except Exception as ex:
            app_log.error(f"Can not create session: {ex}")

    def close_session(self):
        """
        Close connection to db
        """
        try:
            if self._session is not None:
                self._session.close()
                app_log.debug(f"Session `{self.db_name}` closed ")
        except Exception as ex:
            app_log.error(f"Can not close session: {ex}")

    def close_engine(self):
        """
        Close the db engine
        """
        try:
            self.db_engine.dispose()
            app_log.debug("db Engine disposed ")
        except Exception as ex:
            app_log.error(f"Engine NOT disposed: {ex}")

    def insert_entry(self, name: str, surname: str):
        try:
            data = MainTable(name=name,
                             surname=surname)
            self._session.add(data)
        except Exception as ex:
            app_log.error(f"Can not insert into main table: {ex}")
        else:
            self._session.commit()
            app_log.debug(f"Data committed to `{MainTable.__tablename__}`")

    @property
    def select_all(self):
        return self._session.query(MainTable).all()


if __name__ == "__main__":
    app_log.info("Create db app starts.")
    a = LocalDb(local_db_name)
    a.create_main_table()
    a.open_session()
    a.close_session()
    a.close_engine()
    app_log.info("Create db app ends")