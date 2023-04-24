import os
from flask import Flask, render_template, redirect, url_for, flash
from sqlalchemy.orm import defer
from werkzeug.security import generate_password_hash

from models import db, Event, User
from datetime import date, time
from base64 import b64encode
from management_routes import management_bp
from user_authentication_routes import user_authentication_bp

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.register_blueprint(management_bp)
app.register_blueprint(user_authentication_bp)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'lucid.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'beyond_course_scope'
db.init_app(app)


@app.route('/')
def home():
    return render_template('home.html');


@app.route('/events')
def events():
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
        return render_template('events/events.html', flyers=flyers, dates=dates, zip=zip, event_ids=event_ids);

    else:
        flash(f'Unable To Load Events', 'error')
        return redirect(url_for('home'))


@app.route('/events/eventDetails/<event_id>', methods=['GET'])
def event_details(event_id):
    curr_event = Event.query.filter_by(event_id=event_id).one()
    flyer = b64encode(curr_event.event_image).decode('utf-8')
    curr_event_date = curr_event.event_date.strftime("%x")
    curr_event_time = curr_event.event_time.strftime("%I:%M %p")
    return render_template('events/eventDetails.html', event=curr_event, currentDate=date.today(), flyer=flyer,
                           date=curr_event_date, time=curr_event_time)


@app.route('/collaborations')
def collaborations():
    return render_template('collaborations/collaborations.html');


@app.route('/about')
def about():
    return render_template('about.html');


@app.route('/events/reviews')
def reviews():
    return render_template('events/reviews.html');


@app.route('/management')
def management():
    return render_template('management/management.html');


@app.route('/management/analytics')
def managementAnalytics():
    return render_template('management/managementanalytics.html');


@app.route('/management/inquiries')
def managementInquiries():
    return render_template('management/managementinquiries.html');


@app.route('/management/users')
def managementUsers():
    return render_template('management/managementusers.html');


@app.route('/client')
def client():
    return render_template('client/client.html');


@app.route('/guest')
def guest():
    return render_template('guest/guest.html');


@app.route('/guest/flag')
def guestFlag():
    return render_template('guest/guestflag.html');


@app.route('/collaborations/contractWorker')
def contractWorker():
    return render_template('collaborations/contractWorker.html');


@app.route('/client/interestForm')
def eventInquiry():
    return render_template('collaborations/eventInquiry.html');


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
                            'event_time': time(16, 30, 0)},
                           {'event_name': 'Halloween Party', 'event_description': 'Dance the night away for only '
                                                                                  '$5, and get your tickets in our '
                                                                                  'bios before the price goes up!',
                            'event_image': image_as_binary[1], 'event_date': date(2023, 2, 15),
                            'event_time': time(18, 30, 0)},
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
                            'event_time': time(14, 30, 0)},
                           ]
        for event in preloadedEvents:
            event = Event(**event)
            db.session.add(event)

        users = [
            {'username': 'client', 'email': 'client@umd.edu', 'first_name': 'Lucid', 'last_name': 'Client',
             'password': generate_password_hash('clientpw', method='sha256'), 'role': 'CLIENT', 'phone': 1234567890,
             'dob': date(2000, 5, 15), 'zipcode': 20783},
            {'username': 'guest', 'email': 'guest@umd.edu', 'first_name': 'Lucid', 'last_name': 'Guest',
             'password': generate_password_hash('guestpw', method='sha256'), 'role': 'GUEST', 'phone': 1234567890,
             'dob': date(2000, 5, 15), 'zipcode': 20783},
            {'username': 'admin', 'email': 'admin@umd.edu', 'first_name': 'Lucid', 'last_name': 'ADMIN',
             'password': generate_password_hash('adminpw', method='sha256'), 'role': 'ADMIN', 'phone': 1234567890,
             'dob': date(2000, 5, 15), 'zipcode': 20783},
        ]


        for each_user in users:
            a_user = User(first_name=each_user['first_name'], last_name=each_user['last_name'],
                          phone=each_user['phone'], email=each_user['email'],
                          dob=each_user['dob'], zipcode=each_user['zipcode'], username=each_user['username'],
                          password=each_user['password'], role=each_user['role'])
            db.session.add(a_user)

        db.session.commit()
    app.run()
