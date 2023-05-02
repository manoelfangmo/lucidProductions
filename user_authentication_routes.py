from flask import render_template, request, Blueprint, redirect, url_for, session

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from models import *

user_authentication_bp = Blueprint('user_authentication', __name__)
from flask_login import current_user, login_user, login_required


@user_authentication_bp.route('/account/createAccount', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form.get('username')
        existing_user = User.query.filter_by(username=username).first()
        user_email = request.form.get('email')
        existing_email = User.query.filter_by(email=user_email).first()
        if existing_user:
            error = 'Username already taken'
            return render_template('createAccount.html', error=error)
        if existing_email:
            error = 'Account Already Exists Please Login'
            return render_template('login.html', error=error)
        else:
            # Get the form data
            first_name = request.form['first_name']
            last_name = request.form['last_name']

            phone = request.form['phone']
            dob = request.form['dob']
            zipcode = request.form['zipcode']
            password = generate_password_hash(request.form['password'], method='sha256')
            user_type = request.form['userType']

            # Create a new User object and add it to the database
            user = User(first_name=first_name, last_name=last_name, phone=phone, email=user_email,
                        dob=datetime.strptime(dob, '%Y-%m-%d').date(), zipcode=zipcode, username=username,
                        password=password, role=user_type)
            db.session.add(user)
            db.session.commit()

        return redirect(url_for(auth_login))

    else:
        return render_template('createAccount.html')


@user_authentication_bp.route('/account/login', methods=['GET', 'POST'])
def auth_login():
    if current_user.is_authenticated:
        return redirect(url_for('user_authentication.user'))
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user exists in the database
        user = User.query.filter_by(username=username).first()
        if user is not None and check_password_hash(user.password, password):
            # Set session variable to indicate user is logged in
            login_user(user)
            session['user_id'] = user.user_id
            # Get the next page from the URL parameter
            next_page = request.form['next']
            # If the next page is set redirect to next page
            if next_page != "None":
                return redirect(next_page)

            else:
                return redirect(url_for('user_authentication.user'))

        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    else:
        need_login_error = request.args.get('error')  # is performing action that their role does not allow
        if need_login_error:
            return render_template('login.html', error=need_login_error);
        else:
            return render_template('login.html');

@user_authentication_bp.route('/account', methods=['GET', 'POST'])
@login_required
def user():
    curr_user = User.query.filter_by(user_id=current_user.user_id).first()
    if request.method == 'GET':
        return render_template('user.html', user_id=curr_user.user_id, first_name=curr_user.first_name,
                               last_name=curr_user.last_name,
                               phone_number=curr_user.phone, email=curr_user.email, date_of_birth=curr_user.dob, zip=curr_user.zipcode, user_role= curr_user.role);
    if request.method == 'POST':
        if 'user_id' in request.form and request.form['user_id']:
            if 'save' in request.form:
                curr_user.first_name = request.form['first_name']
                curr_user.last_name = request.form['last_name']
                curr_user.email = request.form['email']
                curr_user.phone = request.form['phone_number']
                curr_user.zip_code = request.form['zip']
                curr_user.dob = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
                db.session.commit()
            return render_template('user.html', user_id=curr_user.user_id, first_name=curr_user.first_name,
                                   last_name=curr_user.last_name,
                                   phone_number=curr_user.phone, email=curr_user.email, date_of_birth=curr_user.dob,
                                   zip=curr_user.zipcode, user_role=curr_user.role)
