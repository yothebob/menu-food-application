import sqlite3
import ast

con = sqlite3.connect('meals.db')

cur = con.cursor()

# get dictionary out of txt file
dinners = open("dinners_dict.txt","r")
content = dinners.read()
dinner_dict = ast.literal_eval(content)
dinners.close()


#cur.execute("CREATE TABLE dinners (id INTEGER PRIMARY KEY, name TEXT UNIQUE, ingredients TEXT)")
 i = 0
for keys, values in dinner_dict.items():
    print("key",keys,"Values",values)
    i += 1
    cur.execute("INSERT INTO dinners VALUES (?, ?, ?)",(i, keys, values))
