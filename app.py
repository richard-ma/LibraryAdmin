from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<H1>hello</H1>"


@app.route("/book/new")
def book_new():
    return "book:new"


@app.route("/book/update")
def book_update():
    return "book:update"


@app.route("/book/delete")
def book_delete():
    return "book:delete"


@app.route("/book/search")
def book_search():
    return "book:search"


@app.route("/store/new")
def store_new():
    return "store:new"


@app.route("/store/update")
def store_update():
    return "store:update"


@app.route("/store/delete")
def store_delete():
    return "store:delete"


@app.route("/store/search")
def store_search():
    return "store:search"


@app.route("/audience/register")
def audience_register():
    return "audience:register"


@app.route("/audience/login")
def audience_login():
    return "audience:login"


@app.route("/audience/logout")
def audience_logout():
    return "audience:logout"
