from flask import Flask
from flask import render_template
from flask import g
import sqlite3
import os

PROJECT_ROOT = "/home/richardma/PycharmProjects/LibraryAdmin"
DATABASE = os.path.join(PROJECT_ROOT, "data", "libraryadmin.db")


app = Flask(__name__)


@app.before_request
def connect_db():
    db = getattr(g, 'db', None)
    if db is None:
        g.db = sqlite3.connect(DATABASE)


@app.teardown_request
def close_db(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route("/")
def index():
    return "<H1>hello</H1>"


@app.route("/book/new")
def book_new():
    return render_template('book_new.html')


@app.route("/book/update")
def book_update():
    return render_template("book_update.html")


@app.route("/book/delete")
def book_delete():
    return render_template("book_delete.html")


@app.route("/book/search")
def book_search():
    return render_template("book_search.html")


@app.route("/store/new")
def store_new():
    return render_template("store_new.html")


@app.route("/store/update")
def store_update():
    return render_template("store_update.html")


@app.route("/store/delete")
def store_delete():
    return render_template("store_delete.html")


@app.route("/store/search")
def store_search():
    return render_template("store_search.html")


@app.route("/audience/register")
def audience_register():
    return render_template("audience_register.html")


@app.route("/audience/login")
def audience_login():
    return render_template("audience_login.html")


@app.route("/audience/logout")
def audience_logout():
    return "audience:logout"
