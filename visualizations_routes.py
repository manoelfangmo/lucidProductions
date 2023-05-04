from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import func
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from models import db, Event, User, Review, Flag, EventInquiry, ContractWorker
from authorize import role_required
import plotly.express as px
import pandas as pd
import datetime as dt
from sqlalchemy import extract

visualizations_bp = Blueprint('visualizations', __name__)


@visualizations_bp.route('/management/analytics')
@login_required
@role_required(['ADMIN'])
def management_analytics():
    # Average Review Rating
    avg_rating = db.session.query(func.avg(Review.review_rating).label('average rating')).scalar()
    avg_rating_int = int(avg_rating)

    num_event_inquiries = db.session.query(
        func.count(EventInquiry.event_Inquiry_Id).label('number of event inquiries')).scalar()
    num_event_inquiries_int = int(num_event_inquiries)

    num_contract_inquiries = db.session.query(
        func.count(ContractWorker.contract_inquiry_id).label('number of contract work inquiries')).scalar()
    num_contract_inquiries_int = int(num_contract_inquiries)

    num_management_users = db.session.query(
        func.count(User.user_id).filter(User.role == 'ADMIN').label('number of contract work inquiries')).scalar()
    num_management_users_int = int(num_management_users)

    num_guest_users = db.session.query(
        func.count(User.user_id).filter(User.role == 'GUEST').label('number of contract work inquiries')).scalar()
    num_guest_users_int = int(num_guest_users)

    num_client_users = db.session.query(
        func.count(User.user_id).filter(User.role == 'CLIENT').label('number of contract work inquiries')).scalar()
    num_client_users_int = int(num_client_users)

    qry_events_per_month = db.session.query(
        func.strftime('%Y-%m', Event.event_date).label('Month'),
        func.count(Event.event_id).label('Events Scheduled')
    ) \
        .group_by('Month') \
        .order_by('Month') \
        .all()

    df_events_per_month = pd.DataFrame(qry_events_per_month, columns=['Month', 'Events Scheduled'])

    events_per_month_fig = px.line(df_events_per_month, x="Month", y="Events Scheduled",
                                   color_discrete_sequence=px.colors.qualitative.Antique,
                                   title="Number of Events Scheduled per Month", markers=True,
                                   labels={'Month': '', 'Events Scheduled': 'Events Scheduled'})

    events_per_month_fig.update_layout(
        title={'x': 0.5},
        margin=dict(l=20, r=20, t=40, b=20)
    )

    events_per_month_figJSON = events_per_month_fig.to_json()

    return render_template('management/managementanalytics.html', rating=avg_rating_int,
                           num_event_inquiries=num_event_inquiries_int,
                           num_contract_inquiries=num_contract_inquiries_int,
                           num_management_users=num_management_users_int, num_guest_users=num_guest_users_int,
                           num_client_users=num_client_users_int,
                           events_per_month_graph=events_per_month_figJSON)
