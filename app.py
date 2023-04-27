import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_required, current_user, logout_user
from sqlalchemy.orm import defer
from werkzeug.security import generate_password_hash
from visualizations_routes import visualizations_bp
from authorize import role_required
from models import db, Event, User, Review, Flag, EventInquiry
from datetime import date, time, datetime
from base64 import b64encode
from management_routes import management_bp
from user_authentication_routes import user_authentication_bp
from user_authentication_routes import auth_login

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.register_blueprint(management_bp)
app.register_blueprint(user_authentication_bp)
app.register_blueprint(visualizations_bp)

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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'You have been logged out.', 'success')
    return redirect(url_for('home'))
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
        user_is_guest = False
        if current_user.is_authenticated and current_user.role == "GUEST":
            user_is_guest = True
        return render_template('events/events.html', flyers=flyers, dates=dates, zip=zip, event_ids=event_ids, user_is_guest=user_is_guest);

    else:
        flash(f'Unable To Load Events', 'error')
        return redirect(url_for('home'))
@app.route('/events/flagEvent', methods=['POST'])
@login_required
@role_required(['GUEST'])
def flag_event():
    user_id = current_user.user_id
    event_id = request.form['event_id']
    flag = Flag(user_id=user_id,event_id=event_id)
    db.session.add(flag)
    db.session.commit()
    return "Event Flagged Successfully"
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

@app.route('/events/eventDetails/<event_id>', methods=['GET'])
def event_details(event_id):
    curr_event = Event.query.filter_by(event_id=event_id).one()
    flyer = b64encode(curr_event.event_image).decode('utf-8')
    curr_event_date = curr_event.event_date.strftime("%x")
    curr_event_time = curr_event.event_time.strftime("%I:%M %p")
    user_is_guest = False
    if current_user.is_authenticated and current_user.role == "GUEST":
        user_is_guest = True
    return render_template('events/eventDetails.html', event=curr_event, currentDate=date.today(), flyer=flyer,
                           date=curr_event_date, time=curr_event_time, event_id=event_id, user_is_guest=user_is_guest)



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

    return redirect(url_for('event_details',event_id=event_id))


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


@app.route('/guest', methods=['GET', 'POST'])
def guest():
   user = User.query.filter_by(user_id=2).first()
   if request.method == 'GET':
       return render_template('guest/guest.html', user_id=user.user_id, first_name=user.first_name,
                              last_name=user.last_name,
                              phone_number=user.phone, email=user.email, date_of_birth=user.dob, zip=user.zipcode);
   if request.method == 'POST':
       if 'user_id' in request.form and request.form['user_id']:
           curr_user = User.query.filter_by(user_id=request.form.get('user_id')).one()
           if 'save' in request.form:
               curr_user.first_name = request.form['first_name']
               curr_user.last_name = request.form['last_name']
               curr_user.email = request.form['email']
               curr_user.phone = request.form['phone_number']
               curr_user.zip_code = request.form['zip']
               curr_user.dob = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
               db.session.commit()
           return render_template('guest/guest.html', user_id=curr_user.user_id, first_name=curr_user.first_name,
                                  last_name=curr_user.last_name,
                                  phone_number=curr_user.phone, email=curr_user.email, date_of_birth=curr_user.dob, zip=curr_user.zipcode);

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


@app.route('/client/contractWorker', methods = ['GET', 'POST'])
def contractWorker():
    if request.method == 'POST':
        print('Event type entered: ' + request.form.get('eventType'))
        print('Name entered: ' + request.form.get('name'))
        print('Email entered: ' + request.form.get('email'))
        print('Occupation entered: ' + request.form.get('occupation'))
        print('Work sample entered: ' + request.form.get('sample'))

    return render_template('collaborations/contractWorker.html');


@app.route('/client/interestForm', methods = ['GET', 'POST'])
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
        event_inquiry = EventInquiry(event_type=event_type, user_id=user_id, name=name, company=company, email=email, phone=phone, event_needs=event_needs)
        db.session.add(event_inquiry)
        db.session.commit()
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
