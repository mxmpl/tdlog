from flask import Flask
from flask import request
from flask import render_template
import pandas as pd
import csv
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/ouvrier0", methods=["POST"])
def assigner_chantier_a_ouvrier0():
    ouvriers = pd.read_csv("employes.csv", header = 0)
    chantiers = pd.read_csv("chantiers.csv", index_col = "Nom", sep=",")
    chantier_a_traiter = request.form["chantier_pour_ouvrier0"]
    chantiers.at[chantier_a_traiter,"Ouvrier"] = ouvriers.at[0,"Nom"]
    chantiers.to_csv("chantiers.csv", sep=",")
    return render_template("home.html")


@app.route("/ouvrier1", methods=["POST"])
def assigner_chantier_a_ouvrier1():
    ouvriers = pd.read_csv("employes.csv", header = 0)
    chantiers = pd.read_csv("chantiers.csv", index_col = "Nom", sep=",")
    chantier_a_traiter = request.form["chantier_pour_ouvrier1"]
    chantiers.at[chantier_a_traiter,"Ouvrier"] = ouvriers.at[1,"Nom"]
    chantiers.to_csv("chantiers.csv", sep=",")
    return render_template("home.html")


@app.route("/ouvrier2", methods=["POST"])
def assigner_chantier_a_ouvrier2():
    ouvriers = pd.read_csv("employes.csv", header = 0)
    chantiers = pd.read_csv("chantiers.csv", index_col = "Nom", sep=",")
    chantier_a_traiter = request.form["chantier_pour_ouvrier2"]
    chantiers.at[chantier_a_traiter,"Ouvrier"] = ouvriers.at[2,"Nom"]
    chantiers.to_csv("chantiers.csv", sep=",")
    return render_template("home.html")


@app.route("/affichage_planning")
def affichage_planning(): 
    chantiers = pd.read_csv("chantiers.csv", index_col = "Nom", sep=",")
    html = chantiers.to_html()
    text_file = open("templates/dataframe.html", "w")
    text_file.write(html)
    text_file.close()
    return render_template("dataframe.html")
         

if __name__ == "__main__":
    app.run()

