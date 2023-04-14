from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Event(db.Model):
    __tablename__ = "event"

    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(30), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    event_description = db.Column(db.String(500), nullable=False)
    event_address = db.Column(db.String(50), nullable=False)
    event_theme = db.Column(db.String(50), nullable=False)

    def __init__(self, event_name, event_date, event_description, event_address, event_theme):
        self.event_name = event_name
        self.event_date = event_date
        self.event_description = event_description
        self.event_address = event_address
        self.event_theme = event_theme

    def __repr__(self):
        return f"{self.event_name}"
