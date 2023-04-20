from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary
from flask_login import UserMixin

db = SQLAlchemy()


class Event(db.Model):
    __tablename__ = "event"

    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(30), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    event_description = db.Column(db.Text, nullable=False)
    event_image = db.Column(LargeBinary, nullable=False)
    event_time = db.Column(db.Time, nullable=False)

    def __init__(self, event_name, event_date, event_description, event_image, event_time):
        self.event_name = event_name
        self.event_date = event_date
        self.event_description = event_description
        self.event_image = event_image
        self.event_time = event_time

    def __repr__(self):
        return f"{self.event_name}"


class User(UserMixin, db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.Integer, nullable=False)


    def __init__(self, username, first_name, last_name, email, password, dob, zipcode, role, phone):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role = role
        self.dob = dob
        self.zipcode = zipcode
        self.phone = phone

    # Function for flask_login manager to provider a user ID to know who is logged in
    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
