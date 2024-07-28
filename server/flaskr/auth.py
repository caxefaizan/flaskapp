import functools, re
from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.visitors import increment_visitor_count, get_visitor_count
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def is_valid_email(email):
    # Regular expression for validating email addresses
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False

@bp.route('/register', methods=('GET', 'POST'))
def register():
    count = get_visitor_count()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'
        elif not is_valid_email(email):
            error = 'Enter a valid email.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, email) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), email),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                flash("Registered Successfully")
                return redirect(url_for("auth.login"))

        flash(error)
    else:
        increment_visitor_count()
    return render_template('auth/register.html', visitor_count=count)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    count = get_visitor_count()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None or not check_password_hash(user['password'], password):
            error = 'User and/or Password Incorrect.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            db.execute(
                f"UPDATE user SET lastActivity = ? WHERE username = '{username}'",
                (
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
            db.commit()
            return redirect(url_for('blog.index', username=user['username']))

        flash(error)
    else:
        increment_visitor_count()
    return render_template('auth/login.html', visitor_count=count)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully")
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view