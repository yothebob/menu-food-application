import sqlite3
import ast

con = sqlite3.connect('meals.db')

cur = con.cursor()

# get dictionary out of txt file
dinners = open("dinner_dict.txt","r")
content = dinners.read()
dinner_dict = ast.literal_eval(content)
dinners.close()
