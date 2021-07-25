import re
from bs4 import BeautifulSoup
import requests

r = requests.get('https://based.cooking/')
based_cooking = r.text
soup = BeautifulSoup(based_cooking,'html.parser')

recipes = {}
links = []
for recipe in soup.find_all("li"):
    #finding recipe names, then adding to dict
    cut_end = str(recipe)[0:-9]
    first_letter_index = cut_end.rfind('">')
    recipe_name = cut_end[first_letter_index+2:]
    #print(recipe_name)
    recipes[recipe_name] = []
    #finding recipe html
    cut_left_html = str(recipe)[12:]
    right_quotation = cut_left_html.rfind('"')
    recipe_html = cut_left_html[1:right_quotation]
    #go into recipe html to get ingredients
    links.append(str(recipe_html))

for link in links:
    recipe_r = requests.get('https://based.cooking/' + str(link))
    text = recipe_r.text
    recipe_soup = BeautifulSoup(text,'html.parser')
    recipe_name = recipe_soup.find_all("h1")
    recipe_ingredient_list = recipe_soup.find_all("ul")
    recipe_ingredient_list = str(recipe_ingredient_list).split("</li>")
    recipe_ingredients = []
    for item in recipe_ingredient_list:
        recipe_ingredients.append(item[5:])
    recipe_name = str(recipe_name)[5:-6]
    recipes[str(recipe_name)] = recipe_ingredients
print(recipes)
f = open("based_cooking_scrape.txt","w")
f.write(str(recipes))
f.close()
print("FINISHED!!!!")
