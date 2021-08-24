from flask import Flask, render_template, request, g, url_for
import sqlite3
from menumaker import MenuMaker
import re


app = Flask(__name__)
app.config['SECRET KEY'] = '1233456789'
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


@app.route("/menu/",methods=['GET','POST'])
def create_menu():
    meals = [re.sub(r"[)',(]","",str(meal)) for meal in query_db('SELECT name from dinners')]
    return render_template('menus.html',meals=meals)


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
