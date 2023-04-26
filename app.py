import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_required
from sqlalchemy.orm import defer
from werkzeug.security import generate_password_hash

from authorize import role_required
from models import db, Event, User
from datetime import date, time, datetime
from base64 import b64encode
from management_routes import management_bp
from user_authentication_routes import user_authentication_bp
from user_authentication_routes import auth_login

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.register_blueprint(management_bp)
app.register_blueprint(user_authentication_bp)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'lucid.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'beyond_course_scope'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login' # default login route
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@app.route('/login', methods=['GET', 'POST'])
def login():
    return auth_login()

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
                           date=curr_event_date, time=curr_event_time, event_id=event_id)


@app.route('/collaborations')
def collaborations():
    return render_template('collaborations/collaborations.html');


@app.route('/about')
def about():
    return render_template('about.html');


@app.route('/events/reviews', methods=['POST'])
def reviews():
    print("event_rating" + " " + request.form['review_rating'])
    print("event_id" + " " +request.form['event_id'])
    event_id = request.form['event_id']

    return redirect(url_for('event_details',event_id=event_id));


@app.route('/management')
def management():
    return render_template('management/management.html');


@app.route('/management/analytics')
@login_required
@role_required(['ADMIN'])
def managementAnalytics():
    return render_template('management/managementanalytics.html');


@app.route('/management/inquiries')
@login_required
@role_required(['ADMIN'])
def managementInquiries():
    return render_template('management/managementinquiries.html');


@app.route('/management/users')
@login_required
@role_required(['ADMIN'])
def managementUsers():
    return render_template('management/managementusers.html');


@app.route('/client',methods={'GET','POST'})
@login_required
@role_required(['CLIENT'])
def client():
    user = User.query.filter_by(user_id=1).first()
    return render_template('client/client.html', user_id=user.user_id, first_name=user.first_name,
                                   last_name=user.last_name, phone=user.phone, email=user.email, dob=user.dob,
                                   zipcode=user.zipcode);


@app.route('/guest')
def guest_view_all():
    guests = User.query.order_by(User.user_id) \
        .all()
    return render_template('guest/guest.html', guests=guests);

@app.route('/guest/<int:user_id>')
def guest_view(user_id):
    guests = User.query.filter_by(user_id=user_id)

    if guests:
        return render_template('guest/guest.html', guests=guests, action=os.read);
    else:
        flash(f'Guest attempting to be viewed could not be found!', 'error')
        return redirect(url_for(guest_view_all))

@app.route('/guest/update/<int:user_id>', methods=['GET', 'POST'])
def guest_edit(user_id):
    if request.method == 'GET':
        guest = User.query.filter_by(user_id=user_id)

        if guest:
            return render_template('guest/guest_update.html', guest=guest, action='update')

        else: flash(f'Guest attempting to be edited could not be found!')

    elif request.method == 'POST':
        guest = User.query.filter_by(user_id=user_id)\

        if guest:
            guest.first_name = request.form['first_name']
            guest.last_name = request.form['last_name']
            guest.email = request.form['email']
            guest.dob = request.form['dob']
            guest.zipcode = request.form['zipcode']

            db.session.commit()
            flash(f'{guest.first_name}{guest.last_name} was successfully updated!' 'success')
        else:
            flash(f'Guest attempting to be edited could not be found!', 'error')
            return redirect(url_for('guest_view'))


    return redirect(url_for('guest_view'))

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


@app.route('/guest/flag/<user_id>')
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
            {'username': 'client', 'email': 'client@umd.edu', 'first_name': 'Lucid', 'last_name': 'CLIENT',
             'password': generate_password_hash('clientpw', method='sha256'), 'role': 'CLIENT', 'phone': 1234567890,
             'dob': date(2000, 5, 15), 'zipcode': 20783},
            {'username': 'guest', 'email': 'guest@umd.edu', 'first_name': 'Lucid', 'last_name': 'GUEST',
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
