from flask import Flask
from flask import render_template
from flask import g
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import abort
from flask import flash
from flask import Blueprint
import sqlite3
from hashlib import md5
from datetime import datetime
from flask_bootstrap import Bootstrap5
from flask_login import LoginForm

from helper import *


class Admin:
    def __init__(self, user_id):
        self.id = user_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')


@admin.route('/')
def index():
    return redirect(url_for('.dashboard'))


@admin.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')


@admin.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)
