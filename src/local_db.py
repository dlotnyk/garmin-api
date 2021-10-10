import sqlalchemy as db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
import datetime
import os
from typing import List, Tuple

from logger import log_settings
from table_scheme import MainTable, main_table_name, Base
from garmin_comm import MyGarmin

app_log = log_settings()
local_db_name = "common.db"


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


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
                                db.Column("date", db.Date, index=True, unique=True),
                                db.Column("actCalories", db.Float, nullable=True),
                                db.Column("actSeconds", db.Integer, nullable=True),
                                db.Column("highActSeconds", db.Integer, nullable=True),
                                db.Column("maxHr", db.Integer, nullable=True),
                                db.Column("minHr", db.Integer, nullable=True),
                                db.Column("sleepSeconds", db.Integer, nullable=True)
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

    def insert_entry(self, date: datetime.date, act_calories: float, act_seconds: int,
                     high_act_seconds: int, max_hr: int, min_hr: int, sleep_seconds: int):
        try:
            data = MainTable(date=date,
                             act_calories=act_calories,
                             act_seconds=act_seconds,
                             high_act_seconds=high_act_seconds,
                             max_hr=max_hr,
                             min_hr=min_hr,
                             sleep_seconds=sleep_seconds)
            self._session.add(data)
            self._session.commit()
        except IntegrityError:
            app_log.warning(f"Item: {date} already in db")
            self._session.rollback()
        except Exception as ex:
            app_log.error(f"Can not insert into main table: {ex}")
        else:
            app_log.info(f"Data: {date} committed to `{MainTable.__tablename__}`")

    @property
    def select_all(self):
        return self._session.query(MainTable).all()


if __name__ == "__main__":
    app_log.info("Create db app starts.")
    start_date = datetime.date(2021, 10, 8)
    end_date = datetime.date(2021, 10, 9)
    garm = MyGarmin()
    garm.connect()
    ldb = LocalDb(local_db_name)
    ldb.create_main_table()
    ldb.open_session()
    for tday in daterange(start_date, end_date):
        garm.get_stats(tday.strftime("%Y-%m-%d"))
        ldb.insert_entry(date=garm.get_date,
                        act_calories=garm.get_active_calories,
                        act_seconds=garm.get_active_seconds,
                        high_act_seconds=garm.get_high_active_seconds,
                        max_hr=garm.get_max_hr,
                        min_hr=garm.get_min_hr,
                        sleep_seconds=garm.get_sleep_seconds)
    ldb.close_session()
    ldb.close_engine()
    app_log.info("Create db app ends")