# food program
import random   
from docx import Document

dinners = ['terriki tofu', 'spagetti', 'mac and cheese', 'burritos', 'butternut squash', 'eggplant parmagan', 'lasauna']

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
        p.add_run(menu[day])
    doc.save("menu.docx")
    
    
create_docx(create_menu())
