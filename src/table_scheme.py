import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

main_table_name = "main_table"


class MainTable(Base):
    """
    The main Table
    """
    __tablename__ = main_table_name
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True, unique=True, nullable=False)
    actCalories = db.Column(db.Float, nullable=True)
    actSeconds = db.Column(db.Integer, nullable=True)
    highActSeconds = db.Column(db.Integer, nullable=True)
    maxHr = db.Column(db.Integer, nullable=True)
    maxAvgHr = db.Column(db.Integer, nullable=True)
    minHr = db.Column(db.Integer, nullable=True)
    minAvgHr = db.Column(db.Integer, nullable=True)
    restHr = db.Column(db.Integer, nullable=True)
    sleepSeconds = db.Column(db.Integer, nullable=True)

    def __init__(self, id, date, act_calories, act_seconds, high_act_seconds,
                 max_hr, max_avg_hr, min_hr, min_avg_hr, rest_hr,
                 sleep_seconds):
        self.id = id
        self.date = date
        self.actCalories = act_calories
        self.actSeconds = act_seconds
        self.highActSeconds = high_act_seconds
        self.maxHr = max_hr
        self.maxAvgHr = max_avg_hr
        self.minHr = min_hr
        self.minAvgHr = min_avg_hr
        self.restHr = rest_hr
        self.sleepSeconds = sleep_seconds

    def __repr__(self):
        return "MainTable"
