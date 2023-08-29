import pandas as pd
from flask import Flask, request, render_template
from model import rec_network

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def submit():
    if request.method == 'POST':
        search = request.form.get('search')
        network = rec_network()
        recs = network.train_model()
        rec = network.get_recommendation(recs, search)
        del rec[search.replace(" ", "_")]

        print(rec.get(0))

        name = rec.keys()[0].replace("_", " ")
        simscore = str(round(rec.get(0) * 100, 3)) + "%"
        ingredients = network.get_ingredients(name)
        print(ingredients)
        instructions = network.get_instructions(name)
        ing_keys = []
        print("keys: " + str(ingredients.keys()))
        for i in range(len(ingredients)):
            ing_keys.append(list(ingredients.keys())[i])

       
    else:
        name = None
        ingredients = None
        ing_keys = None
        instructions = None
        simscore=None
        
    return render_template('index.html', name=name, ing_keys=ing_keys, ing=ingredients, ins=instructions, score=simscore)

if __name__ == '__main__':
    app.run()