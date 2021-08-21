from flask import Flask, render_template, request, g, url_for
import sqlite3
from menumaker import MenuMaker


app = Flask(__name__)
DATABASE = 'meals.db'


def get_db():
    db = getattr(g,'_database',None)
    if db is None:
        db = g.database = sqlite3.connect(DATABASE)
    return db


def query_db(query,args=(), one=False):
    cur = get_db().execute(query,args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/menu/")
def create_menu():
    return render_template('index.html')


@app.route("/export/")
def create_docx():
    return render_template("index.html")


@app.route("/grocery/")
def create_grocery_list():
    return render_template("index.html")


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    app.run()
