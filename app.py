import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Event
from datetime import datetime as dt

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../team11spring2023bmgt407/event.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'beyond_course_scope'
db.init_app(app)


@app.route('/')
def home():
    return render_template('home.html');


@app.route('/events')
def events():
    return render_template('events/events.html');


@app.route('/events/futureEventDetails')
def futureEvents():
    return render_template('events/futureEventDetails.html');


@app.route('/events/pastEventDetails')
def past_events():
    return render_template('events/pastEventDetails.html');


@app.route('/account/createAccount', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        return render_template('createAccount.html', form_submitted=True)
    else:
        return render_template('createAccount.html')


@app.route('/account/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html');


@app.route('/management/eventView')
def event_view_all():
    events = Event.query.order_by(Event.event_id) \
        .all()
    return render_template('management/event_view_all.html', events=events)


@app.route('/management/eventView/<int:event_id>')
def event_view(event_id):
    event = Event.query.order_by(Event.event_id) \
        .all()

    if event:
        return render_template('management/event_entry.html', event=event, action='read')

    else:
        flash(f'Event attempting to be viewed could not be found!', 'error')
        return redirect(url_for('management/event_view_all'))


@app.route('/management/eventCreate', methods=['GET', 'POST'])
def event_create():
    if request.method == 'GET':
        return render_template('management/event_entry.html', action='create')
    elif request.method == 'POST':
        event_name = request.form['event_name']
        event_date = dt.strptime(request.form['event_date'], '%Y-%m-%d')
        event_description = request.form['event_description']
        event_theme = request.form['event_theme']

        event = Event(event_name=event_name, event_date=dt.strptime(str(event_date), '%Y-%m-%d %H:%M:%S').date(),
                      event_description=event_description, event_theme=event_theme)
        db.session.add(event)
        db.session.commit()
        flash(f'{event_name} was successfully added!', 'success')
        return redirect(url_for('event_view_all'))

    flash('Invalid action. Please try again.', 'error')
    return redirect(url_for('event_view_all'))


@app.route('/management/eventUpdate/<int:event_id>', methods=['GET', 'POST'])
def event_edit(event_id):
    if request.method == 'GET':
        event = Event.query.filter_by(event_id=event_id).first()
        event = event.__dict__
        if event_id:
            return render_template('management/event_entry.html', event_id=event_id, event=event, action='update')

        else:
            flash(f'Event attempting to be edited could not be found!', 'error')

    elif request.method == 'POST':
        event = Event.query.filter_by(event_id=event_id)
        event.event_name = request.form['event_name']
        event.event_date = dt.strptime(request.form['event_date'], '%Y-%m-%d')
        event.event_description = request.form['event_description']
        event.event_theme = request.form['event_theme']

        db.session.commit()
        flash(f'{event.event_name} was successfully updated!', 'success')


        return redirect(url_for('event_view_all'))

    return redirect(url_for('event_view_all'))


@app.route('/management/eventDelete/<int:event_id>')
def event_delete(event_id):
    event = Event.query.filter_by(event_id=event_id).first()

    if event:
        db.session.delete(event)
        db.session.commit()
        flash(f'{event} was successfully deleted!', 'success')
    else:
        flash(f'Delete failed! Event could not be found.', 'error')

    return redirect(url_for('event_view_all'))


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

    app.run()
