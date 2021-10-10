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
    date = db.Column(db.DateTime, index=True, unique=True)
    actCalories = db.Column(db.Float, nullable=True)
    actSeconds = db.Column(db.Integer, nullable=True)
    highActSeconds = db.Column(db.Integer, nullable=True)
    maxHr = db.Column(db.Integer, nullable=True)
    minHr = db.Column(db.Integer, nullable=True)
    sleepSeconds = db.Column(db.Integer, nullable=True)

    def __init__(self, date, act_calories, act_seconds, high_act_seconds, max_hr, min_hr, sleep_seconds):
        self.date = date
        self.actCalories = act_calories
        self.actSeconds = act_seconds
        self.highActSeconds = high_act_seconds
        self.maxHr = max_hr
        self.minHr = min_hr
        self.sleepSeconds = sleep_seconds

    def __repr__(self):
        return "MainTable"
