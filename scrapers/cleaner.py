import ast

""" a data cleaner made for cleaning scraped recipes from based.cooking"""

f = open("cleaned_based_cooking.txt","r")
unclean_string = f.read()
unclean_dict = ast.literal_eval(unclean_string)
f.close()
cleaned_dict = {}

acceptable_measurement_units = ['min','g','box','gal','quart','tbsp','tsp','tablespoon','teaspoon','ounce','oz','cup','lbs','pound','whole','gram']

for key in unclean_dict.keys():
    if len(unclean_dict[key]) > 1:
        cleaned_dict[key] = unclean_dict[key]

f = open("new_cleaned_based_cooking.txt","w")
f.write(str(cleaned_dict))
f.close()
