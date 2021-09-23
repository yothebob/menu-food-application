from flask import Flask, render_template, request, g, url_for
import sqlite3
from menumaker import MenuMaker
import re
from wtforms import Form, SelectField, SubmitField, validators, RadioField,StringField
import ast

app = Flask(__name__)
app.config['SECRET KEY'] = '1233456789'
DATABASE = 'meals.db'


app.static_folder = "static"

def get_db():
    '''
    Input : NA
    Output : db (database)

    function for getting database
    '''
    db = getattr(g,'_database',None)
    if db is None:
        db = g.database = sqlite3.connect(DATABASE)
    return db


def query_db(query,args=(), one=False):
    cur = get_db().execute(query,args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_meals():
    return [re.sub(r"[)',(]","",str(meal)) for meal in query_db('SELECT name from dinners')]


def get_saved_menus():
    #[f"{{re.sub(r"[)',()]","",str(menu))}"for menu in query_db("SELECT name,meals from saved_menus")]
    keys = [name for name in query_db("SELECT name from saved_menus")]
    values = [values for values in query_db("SELECT meals from saved_menus")]
    dict = {}
    for num in range(len(keys)):
        dict[keys[num][0]] = values[num][0]
        print(values[num][0])
    print(dict)
    return dict



def tuple_meals():
    return [(meal[0],meal[0]) for meal in query_db('SELECT name FROM dinners')]


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/menu/",methods=['GET','POST'])
def create_menu():
    saved_menus = {}
    menumaker = MenuMaker()

    class MenuForm(Form):
        menu_name = StringField("Menu Name: ")
        monday = SelectField("Monday", choices=tuple_meals())
        tuesday = SelectField("Tuesday", choices=tuple_meals())
        wednesday = SelectField("Wednesday", choices=tuple_meals())
        thursday = SelectField("Thursday", choices=tuple_meals())
        friday = SelectField("Friday", choices=tuple_meals())
        saturday = SelectField("Saturday", choices=tuple_meals())
        sunday = SelectField("Sunday",choices=tuple_meals())
        submit = SubmitField("Submit")

    form = MenuForm(request.form)
    dow = [form.monday,form.tuesday,form.wednesday,form.thursday,form.friday,form.saturday,form.sunday]
    if request.method == 'POST':
        menu = [day.data for day in dow]
        f = open('saved_menus.txt',"a")
        saved_menus[form.menu_name.data] = menu
        f.write(str(saved_menus)+"\n")
        menumaker.create_docx(saved_menus)
        f.close()

        return render_template('gen_menu.html')
    else:
        return render_template('menus.html',dow=dow,form=form)


@app.route("/export/")
def create_docx():
    f = open("saved_menus.txt","r")
    saved_menus = [line[0:-1] for line in f.readlines()]
    f.close()

    saved_menus_dict = {}
    for item in saved_menus:
        menu_dict = ast.literal_eval(item)
        saved_menus_dict[next(iter(menu_dict))] = menu_dict[next(iter(menu_dict))]
        #print(saved_menus_dict)

    return render_template("export.html",saved_menus_dict=saved_menus_dict)


@app.route("/grocery/", methods=['GET','POST'])
def create_grocery_list():

    menumaker = MenuMaker()

    db_saved_dict = get_saved_menus()

    #this prints key, value as string and list (each val was put in a tuple inside a big tuple)
    #\/\/ reading/writing to txt file will be obsolete soon
    f = open("saved_menus.txt","r")
    saved_menus = [line[:-1] for line in f.readlines()]
    f.close()

    saved_menus_dict = {}
    for weekly_menu in saved_menus:
        menu_dict = ast.literal_eval(weekly_menu)
        saved_menus_dict[next(iter(menu_dict))] = menu_dict[next(iter(menu_dict))]

    tupled_saved_meals = [(key,key) for key in db_saved_dict.keys()]

    class SavedMenuForm(Form):
        saved_menu = SelectField("Saved Menu: ", choices=tupled_saved_meals)
        submit = SubmitField("Submit")

    form = SavedMenuForm(request.form)
    if request.method == 'POST':

        #quick work around db_dict is reurning str instead of list
        db_saved_list = db_saved_dict[form.saved_menu.data]
        db_list = list(db_saved_list)
        #split_db_saved_menu = db_saved_list.split(",")
        #print(split_db_saved_menu)
        #cleaned_split_list = [item.replace("'", "")for item in split_db_saved_menu]

        grocery_list = menumaker.create_grocery_list(db_list)
    else:
        grocery_list = []

    return render_template("grocery_list.html",grocery_list=grocery_list,form=form)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    app.run()
