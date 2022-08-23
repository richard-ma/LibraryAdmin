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
import os
from hashlib import md5
from datetime import datetime
from flask_bootstrap import Bootstrap5

PROJECT_ROOT = os.path.dirname(__file__)
DATABASE = os.path.join(PROJECT_ROOT, "data", "libraryadmin.db")
SECRET_KEY = "development key"
DEBUG = True

admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')


@admin.route('/')
def index():
    return redirect(url_for('.dashboard'))


@admin.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')
