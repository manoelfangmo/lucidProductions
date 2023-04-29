import os

from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import func
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from models import db, Event, User, Review, Flag
from authorize import role_required
import plotly.express as px
import pandas as pd
import datetime as dt

visualizations_bp = Blueprint('visualizations', __name__)


@visualizations_bp.route('/management/analytics')
@login_required
@role_required(['ADMIN'])
def management_analytics():
    avg_rating = db.session.query(func.avg(Review.review_rating).label('average rating')
                                  ) \
        .all()
    print(avg_rating)

    fig = px.bar(avg_rating, y='Average Rating')
    fig.show()
    return render_template('managementanalytics.html')