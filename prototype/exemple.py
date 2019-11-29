from flask import Flask, request, render_template
import pandas as pd
import os 

app = Flask(__name__)
chantiers = ["Champs-sur-Marne", "Creteil", "Saint-Maurice"]

@app.route("/")
def home():
    user = {'username': 'Bernard'}
    return render_template("bienvenue.html", user = user)
    
@app.route("/home")
def editer():
    return render_template("home.html", chantiers=chantiers)

@app.route("/ouvrier", methods=["POST"])
def assigner_chantier_a_ouvrier():
    chantiers = pd.read_csv("chantiers.csv", index_col = "Nom", sep=",")
    chantiers_a_traiter = request.form
    for ouvrier in chantiers_a_traiter.keys():
        chantiers.at[chantiers_a_traiter[ouvrier],"Ouvrier"] = ouvrier
    chantiers.to_csv("chantiers.csv", sep=",")
    return render_template("home.html")

@app.route("/affichage_planning")
def affichage_planning():
    chantiers = pd.read_csv("chantiers.csv", index_col = "Nom", sep=",")
    return chantiers.to_html()
         
@app.route("/reset")
def reset():
    chantiers = pd.read_csv("chantiers.csv", index_col = "Nom", sep=",")
    for i in range(len(chantiers.loc[:,"Ouvrier"])):
        chantiers.loc[:,"Ouvrier"][i] = " "
    chantiers.to_csv("chantiers.csv", sep=",")
    return render_template("home.html")

    



if __name__ == "__main__":
    app.debug = True 
    app.run()

