from flask import Flask
from flask import render_template

app = Flask(__name__)


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
