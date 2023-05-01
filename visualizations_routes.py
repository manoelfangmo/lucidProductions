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
    #df_average_rating = pd.DataFrame(avg_rating, columns=['average rating'])
    #print(avg_rating)

    #average_rating_fig = px.bar(data_frame=df_average_rating, x=None, y=avg_rating,title='Average Guest Review Rating',
    #                               labels={'': '', 'average rating': ''},
     #                              color_discrete_sequence=['#990000', '#000000'],
      #                             text_auto=True)
  #  average_rating_fig.update_layout(
       # yaxis={'tickmode': 'linear', 'dtick': 1},
        #title={'x': 0.5}
   # )

    #average_rating_fig_JSON = average_rating_fig.to_json()
    return render_template('managementanalytics.html', rating=avg_rating)