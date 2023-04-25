from flask import render_template, request, Blueprint, redirect, url_for, session

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from models import *

user_authentication_bp = Blueprint('user_authentication', __name__)



@user_authentication_bp.route('/account/createAccount', methods=['GET','POST'])
def create_account():
    if request.method == 'POST':
        username = request.form.get('username')
        existing_user = User.query.filter_by(username=username).first()
        user_email = request.form.get('email')
        existing_email = User.query.filter_by(email=user_email).first()
        if existing_user:
            error = 'Username already taken'
            return redirect(url_for('user_authentication.create_account', error=error))
        if existing_email:
            error = 'Account Already Exists Please Login'
            return redirect(url_for('user_authentication.login', error=error))
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
                        dob=datetime.strptime(dob, '%Y-%m-%d').date(), zipcode=zipcode,username=username, password=password, role=user_type)
            db.session.add(user)
            db.session.commit()

        return render_template('login.html')

    else:
        return render_template('createAccount.html')

@user_authentication_bp.route('/account/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user exists in the database
        user = User.query.filter_by(username=username).first()
        if user is not None and check_password_hash(user.password, password):
            # Set session variable to indicate user is logged in
            session['user_id'] = user.user_id
            return redirect(url_for('guest_view', user_id=each_user['user_id']))
        else:
            error = 'Invalid username or password'
            return  redirect(url_for('user_authentication.login', error=error))
    else:
        return render_template('login.html');
