import sqlite3
import ast

con = sqlite3.connect('meals.db')

cur = con.cursor()

"""Code for creating Table for dinner recipes """
#
# # get dictionary out of txt file
# dinners = open("dinners_dict.txt","r")
# content = dinners.read()
# dinner_dict = ast.literal_eval(content)
# dinners.close()
#
#
# cur.execute("CREATE TABLE dinners (id INTEGER PRIMARY KEY, name TEXT, ingredients TEXT)")
# i = 1
# for keys, values in dinner_dict.items():
#     print(i,keys,"\n","Values",values)
#     i += 1
#     cur.execute("INSERT INTO dinners VALUES (?, ?, ?)",(i, str(keys), str(values)))
#

"""code for creating saved menus table"""

saved_menus = open("saved_menus.txt","r")
saved_menus_list = [line for line in saved_menus]
saved_menus.close()
#parsing/ creating one big dictionary (I probably could do this without making one big dict...)
#but fuck it though lol

saved_menus_dict = {}
for item in saved_menus_list:
    translated_dict = ast.literal_eval(item)
    saved_menus_dict[next(iter(translated_dict))] = translated_dict[next(iter(translated_dict))]

#cur.execute("CREATE TABLE saved_menus (id INTEGER PRIMARY KEY, name TEXT, meals TEXT)")

p_key = 1
for key, value in saved_menus_dict.items():
    print(p_key,key,value)
    p_key += 1
    cur.execute("INSERT INTO saved_menus VALUES (?, ?, ?)",(p_key,str(key),str(value)))


con.commit()

con.close()
