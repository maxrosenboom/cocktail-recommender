import numpy as np
import pandas as pd
import pickle
import fasttext
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances

class rec_network:

    def remove_spaces(self, string): 
        if type(string) == str:
            return "_".join(string.split())
        elif type(string) == list:
            return ["_".join(n.split()) for n in string]

    def create_corpus(self):
        doc = open("./data/cocktail-instructions.pickle", "w")
        instructions = pickle.load(doc)
        corpus = []

        for key, value in instructions:
            drink = self.remove_spaces(key).replace(" recipe", "")
            ingredient = self.remove_spaces(list(instructions[key].keys()))
            ingredient = ", ".join(ingredient)

            corpus.append(f"{value} {drink} has ingredient {ingredient}")

        corpus = " ".join(corpus)
        corp_doc = open("./data/corpus-ingredients.txt", "w")
        corp_doc.write(corpus)
        corp_doc.close()

    def train_model(self):
        df = pd.read_csv("./data/clean-data.csv", index_col=0, dtype=str)
        df = df.fillna("0")

        model = fasttext.train_unsupervised("./data/corpus-ingredients.txt")
        drinks = [model.get_word_vector(x) for x in df.columns]

        similarity = pd.DataFrame(cosine_similarity(drinks), columns=self.remove_spaces(list(df.columns)), index=self.remove_spaces(list(df.columns)))
        return similarity

    def get_recommendation(self, model, search):
        search = self.remove_spaces(search)
        return model.sort_values(by=[search], ascending=False)[search][:10]
    
    def get_ingredients(self, name):
        recipes = pd.read_pickle(r'./data/cocktail-ingredients.pickle')
        name = name + " recipe"
        print(recipes[name])
        return recipes[name]
    
    def get_instructions(self, name):
        instructions = pd.read_pickle(r'./data/cocktail-instructions.pickle')
        name = name + " recipe"
        return instructions[name]
    