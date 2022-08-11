from flask import Flask
from flask import render_template
from flask import g
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import abort
import sqlite3
import os

PROJECT_ROOT = os.path.dirname(__file__)
DATABASE = os.path.join(PROJECT_ROOT, "data", "libraryadmin.db")
SECRET_KEY = "development key"
DEBUG = True


def result2dict(res):
    assert len(res) > 1
    return [dict(zip(res[0], row)) for row in res[1:]]


def test_login(abortFlg=False):
    if session.get('logged_in'):
        return True
    else:
        if abortFlg:
            abort(401)
        return False


app = Flask(__name__)
app.config.from_object(__name__)


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
    return redirect(url_for("book_search"))


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
    login = test_login()
    print(login)
    cur = g.db.execute("select * from book")
    rows = cur.fetchall()
    return render_template("book_search.html", data=result2dict(rows), login=login)


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


@app.route("/audience/login", methods=['GET', 'POST'])
def audience_login():
    if request.method == 'GET':
        return render_template("audience_login.html")
    elif request.method == 'POST':
        username = request.form['username']
        cur = g.db.execute("select password from audience where id='%s'" % username)
        password = cur.fetchone()[0]
        if password == request.form['password']: # login successful
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return redirect(url_for("audience_login"))
    else:
        raise Exception("Unkown request method: %s" % request.method)


@app.route("/audience/logout")
def audience_logout():
    session.pop('logged_in', None)
    return redirect(url_for("audience_login"))
