from flask_login import current_user
from flask import render_template, flash, current_app
from functools import wraps

def role_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user and current_user.role in roles:
                pass
            else:
                flash('You do not have permission to access this function.', 'error')
                return render_template('access_denied.html')
            if callable(getattr(current_app, "ensure_sync", None)):
                return current_app.ensure_sync(func)(*args, **kwargs)
            return func(*args, *kwargs)
        return wrapper
    return decorator

#The primary function of this code is to verify if the correct user role is accessing a specific function or argument. If the wrong user type is attempting to access the page, they will be redirected to the access denied page.