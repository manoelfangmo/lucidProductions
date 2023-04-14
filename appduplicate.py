import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Event
from datetime import datetime as dt

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'event.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'beyond_course_scope'
db.init_app(app)


@app.route('/student/view')
def student_view_all():
    events = Event.query.order_by(Event.event_id) \
        .all()
    return render_template('student_view_all.html', events=events)


@app.route('/student/view/<int:event_id>')
def student_view(event_id):
    event = Event.query.order_by(Event.event_id) \
        .all()

    if event:
        return render_template('student_entry.html', event=event, action='read')

    else:
        flash(f'Event attempting to be viewed could not be found!', 'error')
        return redirect(url_for('student_view_all'))


@app.route('/student/create', methods=['GET', 'POST'])
def student_create():
    if request.method == 'GET':
        return render_template('student_entry.html', action='create')
    elif request.method == 'POST':
        event_name = request.form['first_name']
        event_date = request.form['date']
        event_description = request.form['event_description']
        event_address = request.form['event_address']
        event_theme = request.form['event_theme']

        event = Event(event_name=event_name, event_date=dt.strptime(event_date, '%Y-%m-%d'),
                      event_description=event_description, event_address=event_address, event_theme=event_theme)

        db.session.add(event)
        db.session.commit()
        flash(f'{event_name} was successfully added!', 'success')
        return redirect(url_for('student_view_all'))

    flash('Invalid action. Please try again.', 'error')
    return redirect(url_for('student_view_all'))


@app.route('/student/update/<int:event_id>', methods=['GET', 'POST'])
def student_edit(event_id):
    if request.method == 'GET':
        event = Event.query.filter_by(event_id=event_id).first()
        event = event.__dict__
        if event_id:
            return render_template('student_entry.html', event_id=event_id, event=event, action='update')

        else:
            flash(f'Student attempting to be edited could not be found!', 'error')

    elif request.method == 'POST':
        event = Event.query.filter_by(event_id=event_id).first()
        event.event_name = request.form['first_name']
        event.event_date = dt.strptime(request.form['date'], '%Y-%m-%d')
        event.event_description = request.form['event_description']
        event.event_address = request.form['event_address']
        event.event_theme = request.form['event_theme']

        db.session.commit()
        flash(f'{event.event_name} was successfully updated!', 'success')
        # else:
        #     flash(f'Event attempting to be edited could not be found!', 'error')

        return redirect(url_for('student_view_all'))

    return redirect(url_for('student_view_all'))


@app.route('/student/delete/<int:event_id>')
def student_delete(event_id):
    event = Event.query.filter_by(event_id=event_id).first()

    if event:
        db.session.delete(event)
        db.session.commit()
        flash(f'{event} was successfully deleted!', 'success')
    else:
        flash(f'Delete failed! Student could not be found.', 'error')

    return redirect(url_for('student_view_all'))


@app.route('/')
def home():
    return redirect(url_for('student_view_all'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run()