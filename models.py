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


class Review(db.Model):
    __tablename__ = "review"
    review_id = db.Column(db.Integer, primary_key=True)
    review_rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text, nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __init__(self, review_rating, review_text, event_id, user_id):
        self.review_rating = review_rating
        self.review_text = review_text
        self.event_id = event_id
        self.user_id = user_id

    def __repr__(self):
        return f"{self.review_text} {self.review_rating}"


class Flag(db.Model):
    __tablename__ = "flag"
    flag_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __init__(self, event_id, user_id):
        self.event_id = event_id
        self.user_id = user_id

    def __repr__(self):
        return f"{self.event_id} {self.user_id}"


class EventInquiry(db.Model):
    __tablename__ = "eventInquiry"

    event_Inquiry_Id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    event_type = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    event_needs = db.Column(db.Text, nullable=False)

    def __init__(self, event_type, name, phone, company, email, event_needs, user_id):
        self.event_type = event_type
        self.user_id = user_id
        self.name = name
        self.company = company
        self.email = email
        self.phone = phone
        self.event_needs = event_needs

    # Function for flask_login manager to provider a user ID to know who is logged in
    def get_id(self):
        return self.eventInquiryId


class ContractWorker(db.Model):
    __tablename__ = "contract_inquiry"

    contract_inquiry_id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    occupation = db.Column(db.String(100), nullable=False)
    sample = db.Column(LargeBinary, nullable=False)
    event_needs = db.Column(db.Text, nullable=False)

    def __init__(self, event_type, name, email, occupation, sample, event_needs):
        self.event_type = event_type
        self.name = name
        self.email = email
        self.occupation = occupation
        self.sample = sample
        self.event_needs = event_needs

    # Function for flask_login manager to provider a user ID to know who is logged in
    def get_id(self):
        return self.contract_inquiry_id
