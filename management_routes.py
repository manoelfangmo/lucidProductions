from io import BytesIO

from flask import render_template, request, flash, Blueprint, send_file, url_for, redirect
from flask_login import login_required
from sqlalchemy.orm import defer

from authorize import role_required
from models import db, Event, EventInquiry, ContractWorker, Review, User
from datetime import date, time, datetime
from base64 import b64encode, b64decode

management_bp = Blueprint('management', __name__)


@management_bp.route('/management/event', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN', 'MANAGER'])
def management_event():
    if request.method == 'POST':
        if "event_id" in request.form and request.form["event_id"]:  ## if updating or deleting event
            curr_event = Event.query.filter_by(event_id=request.form['event_id']).one()
            if 'save' in request.form:
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
                if request.form['user_id'] != "NONE":
                    curr_event.user_id = request.form['user_id']
                if request.files and request.files["event_image"]:
                    curr_event.event_image = request.files.get('event_image').read()
            else:
                db.session.delete(curr_event)

        else:
            event_name = request.form['event_name']
            event_date = request.form['event_date']
            event_description = request.form['event_description']
            event_time = request.form['event_time']
            event_image = request.files.get('event_image').read()
            user_id = None if (request.form['user_id'] == "NONE") else request.form['user_id']
            event = Event(event_name=event_name, event_date=datetime.strptime(event_date, '%Y-%m-%d').date(),
                          event_description=event_description, event_image=event_image,
                          event_time=datetime.strptime(event_time, '%H:%M').time(),
                          user_id=user_id)
            db.session.add(event)
        db.session.commit()
        flash(f'Event was successfully added!', 'success')
    all_events = Event.query.options(defer(Event.event_image)).order_by(Event.event_date).all()
    flyers = []
    for event in all_events:
        flyers.append(b64encode(event.event_image).decode('utf-8'))
    client_users = User.query.filter(User.role == 'CLIENT').all()
    return render_template('management/managementevent.html', flyers=flyers, events=all_events, zip=zip,
                           clients=client_users)
#The above code is for all event creation, which Manager and Admin roles can do. This allows these users to update and delete events that display on the event page. They will be greeted with a success message when complete.

@management_bp.route('/management/inquiries')
@login_required
@role_required(['ADMIN', 'MANAGER'])
def managementInquiries():
    event_inquiry_ids = [event_inquiry.event_Inquiry_Id for event_inquiry in EventInquiry.query.all()]
    contract_inquiry_ids = [contract_worker.contract_inquiry_id for contract_worker in ContractWorker.query.all()]
    return render_template('management/managementinquiries.html', event_inquiries=event_inquiry_ids,
                           contract_inquiries=contract_inquiry_ids);
#This route allows admin and managers to view a list of all event and contract worker inquiries, sorted by inquiry type.

@management_bp.route('/management/inquiries/viewInquiry', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN', 'MANAGER'])
def management_view_inquiry():
    curr_inquiry = EventInquiry.query.filter_by(event_Inquiry_Id=request.args.get('inquiry_id')).one()

    return render_template('management/managementviewinquiry.html', curr_inquiry=curr_inquiry)
#A route that gives more specific information on event inquiries and displays all submitted form information.

@management_bp.route('/management/inquiries/viewContractInquiry', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN', 'MANAGER'])
def management_view_contract_inquiry():
    curr_inquiry = ContractWorker.query.filter_by(contract_inquiry_id=request.args.get('inquiry_id')).one()
    return render_template('management/managementviewinquiry.html', curr_inquiry=curr_inquiry, isContractInquiry=True)
#A route that gives more specific information on contract inquiries and displays all submitted form information.

@management_bp.route('/management/inquiries/viewContractInquiry/sample', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN', 'MANAGER'])
def management_download_sample():
    curr_inquiry = ContractWorker.query.filter_by(contract_inquiry_id=request.args.get('inquiry_id')).one()
    blob_data = curr_inquiry.sample
    return send_file(BytesIO(blob_data), download_name="sample.pdf", as_attachment=True)


@management_bp.route('/management/users/adduser')
@login_required
@role_required(['ADMIN', 'MANAGER'])
def management_add_user():
    return render_template('management/managementaddusers.html')


@management_bp.route('/management/inquiries/viewInquiry/deleteContract', methods=['POST', 'GET'])
@login_required
@role_required(['ADMIN', 'MANAGER'])
def delete_contract_inquiry():
    inquiry_id = request.args.get('contract_inquiry_id')
    inquiry = ContractWorker.query.filter_by(contract_inquiry_id=inquiry_id).first()
    db.session.delete(inquiry)
    db.session.commit()
    flash('Inquiry deleted successfully', 'success')
    return redirect(url_for('management.managementInquiries'))


@management_bp.route('/management/inquiries/viewInquiry/deleteEvent', methods=['POST', 'GET'])
@login_required
@role_required(['ADMIN', 'MANAGER'])
def delete_event_inquiry():
    inquiry_id = request.args.get('event_Inquiry_Id')
    inquiry = EventInquiry.query.filter_by(event_Inquiry_Id=inquiry_id).first()
    db.session.delete(inquiry)
    db.session.commit()
    flash('Inquiry deleted successfully', 'success')
    return redirect(url_for('management.managementInquiries'))


@management_bp.route('/management/reviews', methods=['GET'])
@login_required
@role_required(['ADMIN', 'MANAGER'])
def management_reviews():
    reviews = db.session.query(Review, Event.event_name) \
        .join(Event, Review.event_id == Event.event_id) \
        .all()
    print(reviews)
    return render_template('management/managementreviews.html', reviews=reviews)


@management_bp.route('/managementaccount/delete', methods=['GET', 'POST'])
@login_required
@role_required(['MANAGER'])
def delete_management_user():
    user_id = request.args.get('user_id')  ##if deleting a specific user that is not the current user
    management_user = User.query.filter_by(user_id=user_id).first()
    db.session.delete(management_user)
    db.session.commit()
    return redirect(url_for('managementUsers'))
