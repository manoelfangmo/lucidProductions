from io import BytesIO

from flask import render_template, request, flash, Blueprint,send_file
from flask_login import login_required
from sqlalchemy.orm import defer

from authorize import role_required
from models import db, Event, EventInquiry, ContractWorker
from datetime import date, time, datetime
from base64 import b64encode, b64decode

management_bp = Blueprint('management', __name__)

@management_bp.route('/management/event', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN'])
def management_event():
    if request.method == 'POST':
        if"event_id" in request.form and request.form["event_id"]: ## if updating or deleting event
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
    return render_template('management/managementevent.html', flyers=flyers, events=all_events, zip=zip)


@management_bp.route('/management/inquiries')
@login_required
@role_required(['ADMIN'])
def managementInquiries():
    event_inquiry_ids = [event_inquiry.event_Inquiry_Id for event_inquiry in EventInquiry.query.all()]
    contract_inquiry_ids = [contract_worker.contract_inquiry_id for contract_worker in ContractWorker.query.all()]
    print(contract_inquiry_ids)
    return render_template('management/managementinquiries.html', event_inquiries = event_inquiry_ids, contract_inquiries = contract_inquiry_ids);



@management_bp.route('/management/inquiries/viewInquiry', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN'])
def management_view_inquiry():
    curr_inquiry = EventInquiry.query.filter_by(event_Inquiry_Id=request.args.get('inquiry_id')).one()

    return render_template('management/managementviewinquiry.html', curr_inquiry=curr_inquiry)

@management_bp.route('/management/inquiries/viewContractInquiry', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN'])
def management_view_contract_inquiry():
    curr_inquiry = ContractWorker.query.filter_by(contract_inquiry_id=request.args.get('inquiry_id')).one()
    blob_data = curr_inquiry.sample
    return render_template('management/managementviewinquiry.html', curr_inquiry=curr_inquiry, isContractInquiry=True)

@management_bp.route('/management/inquiries/viewContractInquiry/sample', methods=['GET', 'POST'])
@login_required
@role_required(['ADMIN'])
def management_download_sample():
    curr_inquiry = ContractWorker.query.filter_by(contract_inquiry_id=request.args.get('inquiry_id')).one()
    blob_data = curr_inquiry.sample
    return send_file(BytesIO(blob_data),download_name="sample.pdf", as_attachment=True)

@management_bp.route('/management/users/adduser')
@login_required
@role_required(['ADMIN'])
def management_add_user():
    return render_template('management/managementaddusers.html')