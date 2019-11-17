from flask import Flask
from flask import request
from flask import render_template
import csv


app = Flask(__name__)

nombre_chantiers = 2 

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/", methods=["POST"])
def choix_chantier_ouvier1():
    chantier_ouv1 = request.form["chantierouvrier1"]
    with open('chantiers.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(chantier_ouv1)
    return render_template("home.html")

#@app.route("/", methods=["POST"])
#def choix_chantier_ouvier2():
#    chantier_ouv2 = request.form["chantierouvrier2"]
#    with open('chantiers.csv', 'w', newline='') as csvfile:
#        spamwriter = csv.writer(csvfile, delimiter=' ',
#                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
#        spamwriter.writerow(chantier_ouv2)
#    return render_template("home.html")

@app.route("/affichage_planning")
def affichage_planning(): 
    with open('chantiers.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            num_chantier = ', '.join(row)
    return render_template("planning.html", message=num_chantier)   
         
#@app.route("/", methods=["POST"])
#def text_box():
#    text = request.form["text"]
#    with open("chantiers.csv","a") as open_csv:
#        open_csv.write("\n"+text)
#    df = pandas.read_csv("employes.csv")
#    processed_text = text.upper()
#    return render_template("bienvenue.html" , message = processed_text, employe = df["Nom"][0])



if __name__ == "__main__":
    app.run()
