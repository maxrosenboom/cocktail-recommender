import pandas as pd
import numpy as np
import pickle
import re

# Remove spaces from recipes and replace with underscore to simplify later issues
# Ex: Bloody Mary -> Bloody_Mary
def remove_spaces(string): 
    if type(string) == str:
        return "_".join(string.split())
    elif type(string) == list:
        return ["_".join(n.split()) for n in string]

# Converts fractions into equivalent decimals
# Ex: 1/2 -> 0.5
def converter(num):
    result = []
    for i in num:
        try:
            converted = float(i)
        except ValueError:
            if i[0] == '/':
                i[0] = ''
            n, denom = i.split('/')
            try:
                lead, n = n.split(' ')
                total = float(lead)
            except ValueError:
                total = 0
            fraction = float(n) / float(denom)
            converted = total + fraction
            
        result.append(converted)
        
    return result

# Converts all units found into oz to standardize units
# Ex: 8 cups -> 1 oz
def convert_units(text):
    regex = r"(^[\d -/]+)(oz|ml|cl|tsp|teaspoon|tea spoon|tbsp|tablespoon|table spoon|cup|cups|qt|quart|drop|drops)"
    data = []
    units = {"oz":1,
             "ml":0.033814,
             "cl":0.33814,
             "tsp":0.166667,
             "teaspoon":0.166667,
             "tea spoon":0.166667,
             "tbsp":0.5,
             "tablespoon":0.5,
             "table spoon":0.5,
             "cup":8,
             "cups":8,
             "qt":0.03125,
             "quart":0.03125,
             "drop":0.0016907
            }
    
    for line in text:
        result = re.search(regex, line)
        
        if result:
            amount = result.group(1).strip()
            unit = result.group(2).strip()
            
            if "-" in amount:
                has_range = True
            else:
                has_range = False
                
            amount = re.sub(r"(\d) (/\d)", r"/1/2", amount)
            amount = amount.replace("-", "+").replace(" ", "+").strip()
            amount = re.sub(r"[+]+", "+", amount)
            decimals = converter(amount.split("+"))
            amount = np.sum(decimals)

            if has_range:
                oz = (amount * units[unit]) / 2
            else:
                oz = amount * units[unit]
                
            data.append(str(round(oz, 2)) + " oz")
        else:
            data.append(line)
    return data

def clean_to_csv():
    recipes = open("../data/cocktail-ingredients.pickle", "rb")
    recipes = pickle.load(recipes)
    instructions = open("../data/cocktail-instructions.pickle", "rb")
    instructions = pickle.load(instructions)
    
    data = {}
    
    for key, value in recipes.items():
        data[key.replace(" recipe", "")] = value
    df = pd.DataFrame(data)
    
    df = df.fillna("")
    
    for drink in df.columns:
        df[drink] = convert_units(df[drink])
        
    df.to_csv("../data/clean-data.csv")
    return

if __name__ == "__main__":
    clean_to_csv()