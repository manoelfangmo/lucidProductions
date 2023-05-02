import os

from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import func
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from models import db, Event, User, Review, Flag, EventInquiry
from authorize import role_required
import plotly.express as px
import pandas as pd
import datetime as dt

visualizations_bp = Blueprint('visualizations', __name__)


@visualizations_bp.route('/management/analytics')
@login_required
@role_required(['ADMIN'])
def management_analytics():
    # Average Review Rating
    avg_rating = db.session.query(func.avg(Review.review_rating).label('average rating')).scalar()
    avg_rating_int = int(avg_rating)


    num_event_inquiries = db.session.query(func.count(EventInquiry.event_inquiry_id).label('number of event inquiries')).scalar()
    num_event_inquiries_int = int(num_event_inquiries)
    return render_template('management/managementanalytics.html', rating=avg_rating_int, num_event_inquiries=num_event_inquiries_int)


