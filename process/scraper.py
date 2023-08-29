import requests
import sys
import pickle
from bs4 import BeautifulSoup

sys.setrecursionlimit(5000)

base_url = "http://www.drinksmixer.com/cat/1/"
pages = range(1, 125)

cocktail_urls = []
cocktail_names = []
cocktail_recipes = []
cocktail_ingredients = []

for page in pages:
    print(f"Running scraper for page {page}")
    url = base_url + str(page)
    #print(url)
    request = requests.get(url)
    response = request.text

    parser = BeautifulSoup(response, 'html.parser')
    drinks = parser.find("div", {"class":"m1"}).find("div", {"class":"min"}).find("div", {"class":"clr"}).find("tr")
    page_urls = drinks.find_all("a")
    description = parser.find("div", {"class":"m1"}).find("div", {"class":"min"}).find("div", {"class":"hrecipe"}).find("div", {"class":"summary RecipeDirections"})
    ingredients = parser.find("div", {"class":"m1"}).find("div", {"class":"min"}).find("div", {"class":"hrecipe"}).find("div", {"class":"recipe_data"})

    for url in page_urls:
        cocktail_urls.append(url)
        cocktail_names.append(url.text)
        
    cocktail_recipes.append(description.text)
    cocktail_ingredients.append(ingredients.text)

print(f"Dumping to docs...")
url_doc = open("../data/cocktail-urls.pickle", "wb")
names_doc = open("../data/cocktail-names.pickle", "wb")
rec_doc = open("../data/cocktail-recipes.pickle", "wb")
ing_doc = open("../data/cocktail-ingredients.pickle", "wb")
pickle.dump(cocktail_urls, url_doc)
pickle.dump(cocktail_names, names_doc)
#pickle.dump(cocktail_recipes, rec_doc) #UNCOMMENT BEFORE FINAL SUBMISSION
#pickle.dump(cocktail_ingredients, ing_doc) #UNCOMMENT BEFORE FINAL SUBMISSIOn
url_doc.close()      
names_doc.close()
rec_doc.close()
ing_doc.close()
print("Done!")
