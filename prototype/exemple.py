from flask import Flask
from flask import request
from flask import render_template
import pandas as pd
import os 

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

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
    if os.path.exists("templates/dataframe.html"):
        os.remove("templates/dataframe.html") 
    chantiers = pd.read_csv("chantiers.csv", index_col = "Nom", sep=",")
    html = chantiers.to_html()
    text_file = open("templates/dataframe.html", "w")
    text_file.write(html)
    text_file.close()
    return render_template("dataframe.html")
         

if __name__ == "__main__":
    app.run()

