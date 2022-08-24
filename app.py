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
from hashlib import md5
from datetime import datetime
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager

from helper import *
import admin


def test_login(abortFlg=False):
    if session.get('logged_in'):
        return True
    else:
        if abortFlg:
            abort(401)
        return False


app = Flask(__name__)
app.config.from_object(__name__)
# Blueprint
app.register_blueprint(admin.admin)
# Bootstrap-Flask
bootstrap = Bootstrap5(app)
# Flask-Login
app.secret_key = SECRET_KEY
loginManager = LoginManager()
loginManager.init_app(app)


# https://docs.python.org/2/library/sqlite3.html#sqlite3.Connection.row_factory
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


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


@loginManager.user_loader
def load_user(user_id):
    cur = g.db.execute("select * from admin where id=?", [
        user_id
    ])
    row = cur.fetchone()
    cur.close()
    if len(row) > 0:
        return admin.Admin(user_id)
    else:
        return None


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
    cur = g.db.execute("select * from book")
    rows = cur.fetchall()[1:]
    cur.close()
    return render_template("book_search.html", data=rows, login=login)


@app.route("/store/new/<book_id>", methods=['GET', 'POST'])
def store_new(book_id):
    mode = "new"
    if request.method == 'GET':
        cur = g.db.execute("select * from book where id='%s'" % book_id)
        row = cur.fetchone()
        cur.close()
        return render_template("store_update.html", mode=mode, data=row)
    elif request.method == 'POST':
        book_id = request.form['book_id']
        store_id = md5((book_id+str(datetime.utcnow())).encode('utf-8')) \
            .hexdigest()
        flag = None
        g.db.execute("insert into store (id, book_id, status, flag) values (?, ?, ?, ?)",
                     [
                         store_id,
                         book_id,
                         request.form['status'],
                         flag,
                     ])
        g.db.commit()
        return redirect(url_for('store_search', book_id=book_id))
    else:
        raise Exception("Unkown request method: %s" % request.method)


@app.route("/store/update/<store_id>", methods=['GET', 'POST'])
def store_update(store_id):
    mode = "update"
    if request.method == 'GET':
        cur = g.db.execute("select * from book inner join store where store.id=? and book.id=store.book_id",
                           [
                               store_id,
                           ])
        row = cur.fetchone()
        cur.close()
        return render_template("store_update.html", data=row, mode=mode)
    elif request.method == 'POST':
        store_id = request.form['id']
        flag = request.form['flag']
        g.db.execute("update store set status=?, flag=? where id=?",
                     [
                         request.form['status'],
                         flag,
                         store_id,
                     ])
        g.db.commit()
        return redirect(url_for('store_search', book_id=request.form['book_id']))
    else:
        raise Exception("Unkown request method: %s" % request.method)


@app.route("/store/delete/<book_id>/<store_id>")
def store_delete(book_id, store_id):
    g.db.execute("delete from store where id='%s'" % store_id)
    g.db.commit()
    return redirect(url_for("store_search", book_id=book_id))


@app.route("/store/search/<book_id>", methods=['GET', 'POST'])
def store_search(book_id):
    login = test_login()
    cur = g.db.execute("select * from book inner join store where book.id='%s' and book.id=store.book_id" % book_id)
    rows = cur.fetchall()[1:]
    cur.close()
    return render_template("store_search.html", data=rows, login=login, book_id=book_id)


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
                         [request.form['username'], request.form['password']])
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
        password = cur.fetchone()['password']
        if password == request.form['password']:  # login successful
            session['logged_in'] = username
            return redirect(url_for('index'))
        else:
            return redirect(url_for("audience_login"))
    else:
        raise Exception("Unkown request method: %s" % request.method)


@app.route("/audience/logout")
def audience_logout():
    session.pop('logged_in', None)
    return redirect(url_for("audience_login"))
