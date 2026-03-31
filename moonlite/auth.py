import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from moonlite.db import get_db

bp = Blueprint('auth', __name__, url_prefix = '/auth')

# Runs before view function.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# Registration of new user pass combo
@bp.route('/register', methods = ('GET', 'POST'))
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                # Attempts add username and password hash into SQLite database file
                # Database lib handles escaping input, preventing SQL injection
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"{username} is already a registered username."
            else:
                # Redirects to login if no exception thrown
                return redirect(url_for("auth.login"))
            
        flash(error)

    return render_template('auth/register.html')

# Login using user pass combo
@bp.route('/login', methods = ('GET', 'POST'))
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # Query database for user. If not found, fetchone() returns None.
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = "Username not found."
        # checks plaintext password against stored hash
        elif not check_password_hash(user['password'], password):
            error = "Incorrect password."

        if error = None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

# Logout user
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Wraps the view function in a user login check. Used for views that require a user to be logged in.
def login_required(view):
    
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        
        return view(**kwargs)
    
    return wrapped_view


