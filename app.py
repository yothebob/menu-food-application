# food program
import random   
from docx import Document
from datetime import date
import ast

def import_dinner_dict():
    file = open("dinners_dict.txt", "r")
    contents = file.read()
    res = ast.literal_eval(contents)
    file.close()
    return res

def import_ingredient_profiles():
    f = open('ingredients.txt','r')
    contents = f.read()
    res = ast.literal_eval(contents)
    f.close()
    return res


dinners = import_dinner_dict()
days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
ingredient_profiles = import_ingredient_profiles()


def create_menu():
    menu = []
    res = []
    for key in dinners.keys():
        menu.append(key)
    for num in range(6):
        res.append(random.choice(menu))
    return res

def add_meal():
    new_meal = input("what would you like to add?")
    ingredients = input("what ingredients do you use?")
    ingredient_array = ingredients.split(",")
    print(ingredient_array)
    dinners[new_meal] = ingredient_array
    f = open("dinners_dict.txt", "w")
    f.write(str(dinners)) 
    f.close()
    

def create_docx():
    new_or_saved = input('would you like to use a saved menu? (y/n) \n: ')
    if "y" in new_or_saved.lower():
        menus = read_saved_menus()
        menu_index = []
        i = 0
        for key,val in menus.items():
            print(i,key,val)
            menu_index.append(key)
            i += 1
        pick_meal = input('Which meal would you like to use? pick corrisponding number (0-x) \n: ')
        menu = menus[menu_index[int(pick_meal)]]
    else:
        menu = create_menu()
    doc = Document()
    p = doc.add_paragraph()
    for day in range(6):
        p.add_run( days[day] + ": " + menu[day] + "\n")
    doc.save(str(date.today()) + "menu.docx")
    f = open("menus.txt","a")
    f.write(str(date.today()) + str(menu))
    f.close() 
    

def generate_menu():
    menu = create_menu()
    [print(days[x]+ ': ' + menu[x]) for x in range(len(menu))]
    save = input('does this menu look good to you? (y/n) to save.')
    if save.lower() == "y":
        f = open('saved_menus.txt','a')
        f.write(str(menu) +'|' + str(date.today()))
        f.close()
    
    
def read_saved_menus():
    f = open('saved_menus.txt','r')
    saved_menus = {}
    for line in f:
        menu=[]
        seperate = line.split('|')
        m = seperate[0][1:-1]
        mm = m.split(',')
        for item in mm:
            menu.append(item.strip("' "))
        date = seperate[1]
        saved_menus[date] = menu
    return saved_menus
    

flavor_profile = ['sweet','sour','salt','bitter','acidic','basic','savory','hotness','spiciness','oily','minty'
,'astringent','starchiness','horseradish','creamy','earthy']

def meal_to_vec(meal):
    res_profile = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    profiles = []
    for ingredient in dinners[meal]:
        if ingredient in ingredient_profiles.keys():
            print(ingredient,ingredient_profiles[ingredient])
            profiles.append(ingredient_profiles[ingredient])
        else:
            new_ingredient_profile = []
            print(ingredient)
            for flavor in range(len(flavor_profile)):
                profile = input(f"how {flavor_profile[flavor]} is this? (0-1)")
                new_ingredient_profile.append(float(profile))
            ingredient_profiles[ingredient] = new_ingredient_profile
            f = open('ingredient.txt','w')
            f.write(ingredient_profiles)
            f.close()
    for item in range(len(profiles)):
        for flavor in range(len(res_profile)):
            res_profile[flavor] += profiles[item][flavor]
    for item in res_profile:
        item = item/len(profiles)
    print(res_profile)    
            
meal_to_vec("testing")        
