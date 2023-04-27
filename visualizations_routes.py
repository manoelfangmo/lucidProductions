from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import func
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from authorize import role_required
from models import *
import plotly.express as px
import pandas as pd
import datetime as dt

visualizations_bp = Blueprint('visualizations', __name__)

@visualizations_bp.route('/management/analytics')
@login_required
@role_required(['ADMIN'])
def management_analytics():
    return render_template('management/managementanalytics.html');