import os
import random
from operator import and_

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_required, current_user, logout_user
from sqlalchemy import func
from sqlalchemy.orm import defer
from werkzeug.security import generate_password_hash

from authorize import role_required
from models import db, Event, User, Review, Flag, EventInquiry, ContractWorker
from datetime import date, time, datetime
from base64 import b64encode
from management_routes import management_bp
from user_authentication_routes import user_authentication_bp
from user_authentication_routes import auth_login
import matplotlib.pyplot as plt
import numpy as np
from visualizations_routes import visualizations_bp

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.register_blueprint(management_bp)
app.register_blueprint(user_authentication_bp)
app.register_blueprint(visualizations_bp)
# Above lines establish and link new py files. Separated python files by key differences in order to not have one massive py file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'lucid.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'beyond_course_scope'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'  # default login route
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  #


# loads user from user id in database and becomes able to access across system

@app.route('/login', methods=['GET', 'POST'])
def login():
    return auth_login()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'You have been logged out.', 'success')
    return redirect(url_for('home'))


# routes that handle all login and logout info

@app.route('/')
def home():
    return render_template('home.html');


@app.route('/guest/guestFlag')
@login_required
@role_required(['GUEST'])
def guestFlag():
    user_id = current_user.user_id
    flyers = []
    event_ids = []
    flags = Flag.query.filter_by(user_id=user_id).all()
    flagged_events = {}
    for flag in flags:
        flagged_events[flag.event_id] = flag.event_id
    for event_id in flagged_events.values():
        event = Event.query.filter_by(event_id=event_id).first()
        if event is not None:
            flyers.append(b64encode(event.event_image).decode('utf-8'))
            event_ids.append(event.event_id)
        else:
            # Removes the flag from events
            Flag.query.filter_by(user_id=user_id, event_id=event_id).delete()
            db.session.commit()
            # Remove the event from the list of flagged events
            flagged_events.pop(event_id)
    return render_template('guest/guestflag.html', flyers=flyers, zip=zip, event_ids=event_ids)
    # route that handles flag functionality. ALlows guest users to flag and unflag events they are interested in


@app.route('/events')
def events():
    events = Event.query.options(defer(Event.event_image)).order_by(Event.event_date).all()
    if 'value' in request.args:
        today = date.today()
        if request.args.get('value') == 'past':
            events = Event.query.options(defer(Event.event_image)).filter(Event.event_date < today).order_by(
                Event.event_date).all()
        elif request.args.get('value') == 'upcoming':
            events = Event.query.options(defer(Event.event_image)).filter(Event.event_date > today).order_by(
                Event.event_date).all()
        else:
            events = Event.query.options(defer(Event.event_image)).order_by(Event.event_date).all()

    flyers = []
    dates = []
    event_ids = []
    for event in events:
        dates.append(
            {"weekday": event.event_date.strftime("%a"), "monthday": event.event_date.strftime("%d"),
             "month": event.event_date.strftime("%b")})
        flyers.append(b64encode(event.event_image).decode('utf-8'))
        event_ids.append(event.event_id)
    if events:
        user_is_guest = False
        auth_but_not_guest = False
        if current_user.is_authenticated and current_user.role == "GUEST":
            user_is_guest = True
        if current_user.is_authenticated and current_user.role != "GUEST":
            auth_but_not_guest = True
        return render_template('events/events.html', flyers=flyers, dates=dates, zip=zip, event_ids=event_ids,
                               user_is_guest=user_is_guest, auth_but_not_guest=auth_but_not_guest);

    else:
        flash(f'Unable To Load Events', 'error')
        return redirect(url_for('home'))


# events page route, shows past events sorted by date and  all events that have yet to occur.


@app.route('/events/flagEvent', methods=['POST'])
@login_required
@role_required(['GUEST'])
def flag_event():
    user_id = current_user.user_id
    event_id = request.form['event_id']
    flag = Flag(user_id=user_id, event_id=event_id)
    db.session.add(flag)
    db.session.commit()
    return "Event Flagged Successfully"


# route handling flagging events

@app.route('/events/flagEvent/deleteFlag', methods=['POST'])
@login_required
@role_required(['GUEST'])
def delete_flag_event():
    user_id = current_user.user_id
    event_id = request.form['event_id']
    flag = Flag.query.filter_by(event_id=event_id, user_id=user_id).first()
    db.session.delete(flag)
    db.session.commit()
    return "Flag Deleted Successfully"
@app.route('/guest/guestFlag/delete', methods=['GET','POST'])
@login_required
@role_required(['GUEST'])
def guest_account_delete_flag():
    user_id = current_user.user_id
    event_id = request.args.get('event_id')
    flag = Flag.query.filter_by(event_id=event_id, user_id=user_id).first()
    db.session.delete(flag)
    db.session.commit()
    return redirect(url_for('guestFlag'))

# route handling flag deletion
@app.route('/events/eventDetails/<event_id>', methods=['GET'])
def event_details(event_id):
    curr_event = Event.query.filter_by(event_id=event_id).one()
    flyer = b64encode(curr_event.event_image).decode('utf-8')
    curr_event_date = curr_event.event_date.strftime("%x")
    curr_event_time = curr_event.event_time.strftime("%I:%M %p")
    user_is_guest = False
    auth_but_not_guest = False
    if current_user.is_authenticated and current_user.role == "GUEST":
        user_is_guest = True
    if current_user.is_authenticated and current_user.role != "GUEST":
        auth_but_not_guest = True
    return render_template('events/eventDetails.html', event=curr_event, currentDate=date.today(), flyer=flyer,
                           date=curr_event_date, time=curr_event_time, event_id=event_id, user_is_guest=user_is_guest,
                           auth_but_not_guest=auth_but_not_guest)


# route for more specific event information, specified by event id primary key when clicked on from events page

@app.route('/collaborations')
def collaborations():
    return render_template('collaborations/collaborations.html');


@app.route('/about')
def about():
    return render_template('about.html');


@app.route('/events/reviews', methods=['POST'])
@login_required
@role_required(['GUEST'])
def reviews():
    review_rating = request.form['review_rating']
    review_text = request.form['review_text']

    event_id = request.form['event_id']
    user_id = current_user.user_id

    review = Review(review_rating=review_rating, review_text=review_text, event_id=event_id, user_id=user_id)
    db.session.add(review)
    db.session.commit()

    return redirect(url_for('event_details', event_id=event_id))


# primary code handling reviews, including storing and retrieving guest submitted data through POST request

@app.route('/management')
def management():
    return render_template('management/management.html');


@app.route('/management/analytics')
@login_required
@role_required(['ADMIN','MANAGER'])
def managementAnalytics():
    return render_template('management/managementanalytics.html');


@app.route('/management/users')
@login_required
@role_required(['ADMIN','MANAGER'])
def managementUsers():
    admin_users = User.query.filter(User.role == 'ADMIN').all()
    admin_user_ids = [user.user_id for user in admin_users]
    return render_template('management/managementusers.html', admin_user_ids=admin_user_ids);


@app.route('/management/users/viewUser')
@login_required
@role_required(['ADMIN','MANAGER'])
def management_view_user():
    curr_user = User.query.filter_by(user_id=request.args.get('user_id')).one()
    return render_template('management/managementviewusers.html', curr_user=curr_user);


# route that allows managers to view user details

@app.route('/guest/delete/<int:user_id>')
def guest_delete(user_id):
    guest = User.query.filter_by(user_id=user_id).first()

    if guest:
        db.session.delete(guest)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        flash(f'Delete failed! Guest could not be found.', 'error')
        return redirect(url_for('guest_view'))


@app.route('/client/contractWorker', methods=['GET', 'POST'])
def contractWorker():
    if request.method == 'POST':
        event_type = request.form['event_type']
        name = request.form['name']
        email = request.form['email']
        occupation = request.form['occupation']
        sample = request.files.get('sample').read()
        event_needs = request.form['event_needs']
        contract_inquiry = ContractWorker(event_type=event_type, name=name, email=email, occupation=occupation,
                                          sample=sample, event_needs=event_needs)
        db.session.add(contract_inquiry)
        db.session.commit()
        return render_template('collaborations/contractWorker.html', form_submitted=True);
    else:
        return render_template('collaborations/contractWorker.html');


@app.route('/client/interestForm', methods=['GET', 'POST'])
@login_required
@role_required(['CLIENT'])
def eventInquiry():
    if request.method == 'POST':
        user_id = current_user.user_id
        event_type = request.form['event_type']
        name = request.form['name']
        phone = request.form['phone']
        company = request.form['company']
        email = request.form['email']
        event_needs = request.form['event_needs']
        event_inquiry = EventInquiry(event_type=event_type, user_id=user_id, name=name, company=company, email=email,
                                     phone=phone, event_needs=event_needs)
        db.session.add(event_inquiry)
        db.session.commit()
        return render_template('clientInquiry.html', form_submitted=True);
    else:
        return render_template('clientInquiry.html');


# prior two routes display submission forms for clients and potential contract workers to apply for work or send inquiry to management
@app.route('/client/events')
@login_required
@role_required(['CLIENT'])
def client_events():
    curr_client_events = Event.query.filter_by(user_id=current_user.user_id).all()
    flyers = []
    for event in curr_client_events:
        flyers.append(b64encode(event.event_image).decode('utf-8'))
    return render_template('clientEvents.html', flyers=flyers, events=curr_client_events,zip=zip);

@app.route('/client/reviews')
@login_required
@role_required(['CLIENT'])
def client_reviews():
    curr_client_reviews = db.session.query(Review, Event.event_name).join(Event).filter(Event.user_id == current_user.user_id).all()
    return render_template('management/managementreviews.html', reviews=curr_client_reviews, isClient=True)

@app.route('/accessDenied')
@login_required
def access_denied():
    error = request.args.get('error', None)
    return render_template('access_denied.html', error=error);

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Execute only once! Initial loading of events
        image_list = ['static/images/valentinesParty.jpg', 'static/images/halloweenParty.jpg',
                      'static/images/backToSchoolParty.jpg', 'static/images/comingSoon.jpg']
        image_as_binary = []
        for image in image_list:
            with open(image, 'rb') as file:
                image_as_binary.append(file.read())

        preloadedEvents = [{'event_name': 'Valentine\'s  Party', 'event_description': 'Dance the night away for only '
                                                                                      '$5, and get your tickets in our '
                                                                                      'bios before the price goes up!',
                            'event_image': image_as_binary[0], 'event_date': date(2022, 5, 15),
                            'event_time': time(16, 30, 0), 'user_id': 1},
                           {'event_name': 'Halloween Party', 'event_description': 'Dance the night away for only '
                                                                                  '$5, and get your tickets in our '
                                                                                  'bios before the price goes up!',
                            'event_image': image_as_binary[1], 'event_date': date(2023, 2, 15),
                            'event_time': time(18, 30, 0), 'user_id': 1},
                           {'event_name': 'Back To School  Party', 'event_description': 'Dance the night away for only '
                                                                                        '$5, and get your tickets in our '
                                                                                        'bios before the price goes up!',
                            'event_image': image_as_binary[2], 'event_date': date(2023, 1, 12),
                            'event_time': time(20, 30, 0)},
                           {'event_name': 'Coming Soon', 'event_description': 'Dance the night away for only '
                                                                              '$5, and get your tickets in our '
                                                                              'bios before the price goes up!',
                            'event_image': image_as_binary[3], 'event_date': date(2023, 5, 15),
                            'event_time': time(14, 30, 0)},
                           {'event_name': 'Coming Soon', 'event_description': 'Dance the night away for only '
                                                                              '$5, and get your tickets in our '
                                                                              'bios before the price goes up!',
                            'event_image': image_as_binary[3], 'event_date': date(2023, 5, 15),
                            'event_time': time(14, 30, 0), 'user_id': 1},
                           ]
        for event in preloadedEvents:
            event = Event(**event)
            db.session.add(event)

        users = [
            {'username': 'client', 'email': 'client@umd.edu', 'first_name': 'Lucid', 'last_name': 'CLIENT',
             'password': generate_password_hash('clientpw', method='sha256'), 'role': 'CLIENT', 'phone': 1234567890,
             'dob': date(2000, 5, 15), 'zipcode': 20783},
            {'username': 'guest', 'email': 'guest@umd.edu', 'first_name': 'Lucid', 'last_name': 'GUEST',
             'password': generate_password_hash('guestpw', method='sha256'), 'role': 'GUEST', 'phone': 1234567890,
             'dob': date(2000, 5, 15), 'zipcode': 20783},
            {'username': 'admin', 'email': 'admin@umd.edu', 'first_name': 'Lucid', 'last_name': 'ADMIN',
             'password': generate_password_hash('adminpw', method='sha256'), 'role': 'ADMIN', 'phone': 1234567890,
             'dob': date(2000, 5, 15), 'zipcode': 20783},
            {'username': 'manager', 'email': 'manager@umd.edu', 'first_name': 'Lucid', 'last_name': 'MANAGER',
             'password': generate_password_hash('managerpw', method='sha256'), 'role': 'MANAGER', 'phone': 1234567890,
             'dob': date(2000, 5, 15), 'zipcode': 20783}
        ]

        for each_user in users:
            a_user = User(first_name=each_user['first_name'], last_name=each_user['last_name'],
                          phone=each_user['phone'], email=each_user['email'],
                          dob=each_user['dob'], zipcode=each_user['zipcode'], username=each_user['username'],
                          password=each_user['password'], role=each_user['role'])
            db.session.add(a_user)

        review_text = ["I really enjoyed this event!", "The experience was amazing.",
                       "I had a great time at this event.", "The event was well-organized and fun.",
                       "I would definitely attend this event again.", "This event was a huge disappointment.",
                       "I didn't enjoy this event at all.", "The event was poorly organized and chaotic.", ]

        reviews = []

        for i in range(5):
            rating = random.randint(1, 5)
            text = random.choice(review_text)
            event_id = random.randint(1, 3)

            review = {'review_rating': rating, 'review_text': text, 'event_id': event_id, 'user_id': 2}
            reviews.append(review)

        for each_review in reviews:
            a_review = Review(review_rating=each_review['review_rating'], review_text=each_review['review_text'],
                              event_id=each_review['event_id'], user_id=each_review['user_id'])
            db.session.add(a_review)

        event_types = ['concert', 'conference', 'fundraiser', 'team building', 'trade show', 'other']

        client_needs_text = 'I am looking for a spacious venue to host my upcoming event, and I require the ' \
                            'availability of high-quality audio and video equipment to ensure that my guests can ' \
                            'enjoy a multimedia experience. The venue should be large enough to comfortably ' \
                            'accommodate a sizeable audience, with ample seating and room for equipment setup. The ' \
                            'audio system should be able to deliver clear, crisp sound that can be heard throughout ' \
                            'the space, while the video equipment should be of sufficient quality to provide sharp, ' \
                            'vivid images on a large screen.'
        eventInquiries = [
            {'user_id': 1, 'event_type': random.choice(event_types), 'name': 'John Doe',
             'phone': '2025551234', 'company': 'ABC Inc', 'email': 'johndoe@example.com',
             'event_needs': client_needs_text},
            {'user_id': 1, 'event_type': random.choice(event_types), 'name': 'Jane Smith',
             'phone': '2025555678', 'company': 'XYZ Corp', 'email': 'janesmith@example.com',
             'event_needs': client_needs_text},
            {'user_id': 1, 'event_type': random.choice(event_types), 'name': 'Bob Johnson',
             'phone': '2025559012', 'company': '123 LLC', 'email': 'bobjohnson@example.com',
             'event_needs': client_needs_text}
        ]

        for each_inquiry in eventInquiries:
            a_event_inquiry = EventInquiry(user_id=each_inquiry['user_id'],
                                           event_type=each_inquiry['event_type'], name=each_inquiry['name'],
                                           phone=each_inquiry['phone'], company=each_inquiry['company'],
                                           email=each_inquiry['email'], event_needs=each_inquiry['event_needs'])
            db.session.add(a_event_inquiry)

        document = None
        with open('static/images/resume.pdf', 'rb') as file:
            document = file.read()
        event_needs_text = 'As a contract worker, I am able to provide a wide range of services to ensure the success ' \
                           'of your event. This includes coordinating with vendors and suppliers to source necessary ' \
                           'materials and equipment, setting up and breaking down event spaces, managing event ' \
                           'logistics, and overseeing day-of operations. I am also able to provide event planning and ' \
                           'coordination services, such as developing event themes, creating event timelines, ' \
                           'and managing guest lists. In addition, I have experience in providing technical support ' \
                           'and troubleshooting for event equipment, as well as managing event staff and volunteers.'
        contractWorkerInquiries = [
            {'event_type': random.choice(event_types), 'name': 'John Doe', 'email': 'johndoe@example.com',
             'occupation': 'Event Planner', 'sample': document,
             'event_needs': event_needs_text},
            {'event_type': random.choice(event_types), 'name': 'John Doe', 'email': 'johndoe@example.com',
             'occupation': 'Event Planner', 'sample': document,
             'event_needs': event_needs_text},
            {'event_type': random.choice(event_types), 'name': 'John Doe', 'email': 'johndoe@example.com',
             'occupation': 'Event Planner', 'sample': document,
             'event_needs': event_needs_text}
        ]
        for each_inquiry in contractWorkerInquiries:
            inquiry = ContractWorker(event_type=each_inquiry['event_type'], name=each_inquiry['name'],
                                     email=each_inquiry['email'],
                                     occupation=each_inquiry['occupation'], sample=each_inquiry['sample'],
                                     event_needs=each_inquiry['event_needs'])

            db.session.add(inquiry)

        db.session.commit()
        app.run()

    # Code that allows preloaded data to be entered into lucid database, includes reviews, inquiries, users, and events
