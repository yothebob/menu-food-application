import re 
from bs4 import BeautifulSoup
import requests

r = requests.get('https://based.cooking/')
based_cooking = r.text
soup = BeautifulSoup(based_cooking,'html.parser')

recipes = {}

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
    print(recipe_name,recipe_html)
    recipe_r = requests.get('https://based.cooking/' + str(recipe.html))
    text = recipe_r.text
    recipe_soup = BeautifulSoup(text,'html.parser')
    print("it worked!")
    print(recipe_soup.prettify())
