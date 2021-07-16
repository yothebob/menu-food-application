# food program
import random   
from docx import Document
from datetime import date

def import_dinners():
    res = []
    f = open("dinners.txt","r")
    for line in f:
        res.append(line)
    return res

dinners = import_dinners()

days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def create_menu():
    menu = [random.choice(dinners) for x in range(6)]
    return menu

def add_meal():
    new_meal = input("what would you like to add?")
    dinners.append(new_meal)
    
def create_docx(menu):
    doc = Document()
    p = doc.add_paragraph()
    for day in range(6):
        p.add_run( days[day] + ": " + menu[day] + "\n")
    doc.save(str(date.today()) + "menu.docx")
    f = open("menus.txt","a")
    f.write(str(date.today()) + str(menu))
    f.close() 
    
create_docx(create_menu())

