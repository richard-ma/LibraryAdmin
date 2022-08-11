from flask import Flask
from flask import render_template
from flask import g
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import abort
from flask import flash
import sqlite3
import os
from hashlib import md5

PROJECT_ROOT = os.path.dirname(__file__)
DATABASE = os.path.join(PROJECT_ROOT, "data", "libraryadmin.db")
SECRET_KEY = "development key"
DEBUG = True


# https://docs.python.org/2/library/sqlite3.html#sqlite3.Connection.row_factory
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


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
        g.db.row_factory = dict_factory


@app.teardown_request
def close_db(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route("/")
def index():
    return redirect(url_for("book_search"))


@app.route("/book/new", methods=['GET', 'POST'])
def book_new():
    mode = "new"
    if request.method == 'GET':
        return render_template('book_update.html', mode=mode)
    elif request.method == 'POST':
        book_id = md5((request.form['name']+request.form['author']+request.form['publisher']+request.form['isbn']).encode('utf-8')) \
            .hexdigest()
        flag = None
        g.db.execute("insert into book (id, name, author, publisher, isbn, image, flag) values (?, ?, ?, ?, ?, ?, ?)",
                     [
                         book_id,
                         request.form['name'],
                         request.form['author'],
                         request.form['publisher'],
                         request.form['isbn'],
                         request.form['image'],
                         flag,
                     ])
        g.db.commit()
        return redirect(url_for('book_search'))
    else:
        raise Exception("Unkown request method: %s" % request.method)


@app.route("/book/update/<book_id>", methods=['GET', 'POST'])
def book_update(book_id):
    mode = "update"
    if request.method == 'GET':
        cur = g.db.execute("select * from book where id='%s'" % book_id)
        row = cur.fetchone()
        cur.close()
        return render_template('book_update.html', data=row, mode=mode)
    elif request.method == 'POST':
        book_id = request.form['id']
        flag = request.form['flag']
        g.db.execute("update book set name=?, author=?, publisher=?, isbn=?, image=?, flag=? where id=?",
                     [
                         request.form['name'],
                         request.form['author'],
                         request.form['publisher'],
                         request.form['isbn'],
                         request.form['image'],
                         flag,
                         book_id,
                     ])
        g.db.commit()
        return redirect(url_for('book_search'))
    else:
        raise Exception("Unkown request method: %s" % request.method)


@app.route("/book/delete/<book_id>")
def book_delete(book_id):
    g.db.execute("delete from book where id='%s'" % book_id)
    g.db.commit()
    return redirect(url_for("book_search"))


@app.route("/book/search")
def book_search():
    login = test_login()
    print(login)
    cur = g.db.execute("select * from book")
    rows = cur.fetchall()[1:]
    cur.close()
    return render_template("book_search.html", data=rows, login=login)


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


@app.route("/audience/register", methods=['GET', 'POST'])
def audience_register():
    if request.method == 'GET':
        return render_template("audience_register.html")
    elif request.method == 'POST':
        if request.form['password'] != request.form['repassword']:
            flash("Password and Re-Password are not the same.")
            return redirect(url_for('audience_register'))
        else:
            g.db.execute("insert into audience (id, password) values (?, ?)",
                         [ request.form['username'], request.form['password']])
            g.db.commit()
            return redirect(url_for('audience_login'))
    else:
        raise Exception("Unkown request method: %s" % request.method)


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
