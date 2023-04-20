from flask import render_template, request, flash, Blueprint
from sqlalchemy.orm import defer

from models import db, Event
from datetime import date, time, datetime
from base64 import b64encode, b64decode

management_bp = Blueprint('management', __name__)

@management_bp.route('/management/event', methods=['GET', 'POST'])
def management_event():
    userTest = "management"; #testing user type
    if request.method == 'POST':
        if"event_id" in request.form and request.form["event_id"]: ## if updatinng or deleting event
            curr_event = Event.query.filter_by(event_id=request.form['event_id']).one()
            if 'save' in request.form:
                print(request.files)
                curr_event.event_date = datetime.strptime(request.form['event_date'], '%Y-%m-%d').date()
                time_parts = request.form['event_time'].split(':')
                if len(time_parts) == 3:
                    # the time string includes seconds
                    curr_event.event_time = datetime.strptime(request.form['event_time'], '%H:%M:%S').time()
                else:
                    # the time string doesn't include seconds
                    curr_event.event_time = datetime.strptime(request.form['event_time'], '%H:%M').time()
                curr_event.event_description = request.form['event_description']
                curr_event.event_name = request.form['event_name']
                if request.files and request.files["event_image"]:
                    print("doing this")
                    curr_event.event_image = request.files.get('event_image').read()
            else:
                db.session.delete(curr_event)

        else:
            event_name = request.form['event_name']
            event_date = request.form['event_date']
            event_description = request.form['event_description']
            event_time = request.form['event_time']
            event_image = request.files.get('event_image').read()
            event = Event(event_name=event_name, event_date=datetime.strptime(event_date, '%Y-%m-%d').date(),
                      event_description=event_description, event_image=event_image,
                      event_time=datetime.strptime(event_time, '%H:%M').time()
                      )
            db.session.add(event)
        db.session.commit()
        flash(f'Event was successfully added!', 'success')
    ###to do tomorrow if user is client query client events
    all_events = Event.query.options(defer(Event.event_image)).order_by(Event.event_date).all()
    flyers = []
    for event in all_events:
        flyers.append(b64encode(event.event_image).decode('utf-8'))
    return render_template('management/managementevent.html', flyers=flyers, events=all_events, zip=zip, user=userTest)
