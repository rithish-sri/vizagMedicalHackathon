import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


# REGISTER

@bp.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        name = request.form["name"]
        username = request.form['username']
        password = request.form['password']
        profession = request.form["profession"]
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (name, username, password, profession) VALUES (?, ?, ?, ?)",
                    (name, username, generate_password_hash(password), profession),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)
    msg = ''
    return render_template("register.html", msg='')


# LOGIN
@bp.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('dash.dashboard'))

        flash(error)
    msg = ''
    return render_template("login.html", msg='')


# Loading the details of the logged in user
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


# Logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('/'))


# Requiring authentication
