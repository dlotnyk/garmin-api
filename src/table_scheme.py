import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

main_table_name = "main_table"


class MainTable(Base):
    """
    The main Table
    """
    __tablename__ = main_table_name
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)
    act_calories = db.Column(db.Float, nullable=True)
    act_seconds = db.Column(db.Integer, nullable=True)
    high_act_seconds = db.Column(db.Integer, nullable=True)
    max_hr = db.Column(db.Integer, nullable=True)
    min_hr = db.Column(db.Integer, nullable=True)
    sleep_seconds = db.Column(db.Integer, nullable=True)

    def __init__(self, date, act_calories, act_seconds, high_act_seconds, max_hr, min_hr, sleep_seconds):
        self.date = date
        self.act_calories = act_calories
        self.act_seconds = act_seconds
        self.high_act_seconds = high_act_seconds
        self.max_hr = max_hr
        self.min_hr = min_hr
        self.sleep_seconds = sleep_seconds

    def __repr__(self):
        return "Main Table"
