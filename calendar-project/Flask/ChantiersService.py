from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

attribution = [
{"start":"2020-01-05", "chantier":"Champs-sur-Marn", "ouvrier":"Max"},
{"start":"2020-01-08", "chantier":"Paris", "ouvrier":"Raph"},
{"start":"2020-01-10", "chantier":"Bordeaux", "ouvrier":"Margot"},
{"start":"2020-01-08", "chantier":"Noisy", "ouvrier":"Max2"},
{"start":"2020-01-12", "chantier":"Mulhouse", "ouvrier":"Fredo", "end":"2020-01-15"}
]

test = { "totalItems":5,"items":[
{"start":"2020-01-05", "chantier":"Champs-sur-Marne", "ouvrier":"Max"},
{"start":"2020-01-08", "chantier":"Paris", "ouvrier":"Raph"},
{"start":"2020-01-10", "chantier":"Bordeaux", "ouvrier":"Margot"},
{"start":"2020-01-08", "chantier":"Noisy", "ouvrier":"Max2"},
{"start":"2020-01-12", "chantier":"Mulhouse", "ouvrier":"Fredo", "end":"2020-01-15"}
]
}


for dico in attribution:
    dico["title"] = dico["ouvrier"] + " est a " + dico["chantier"]
    
def set_new_ouvrier(ouvrier):
    global test 
    test["items"].append({"ouvrier":ouvrier})
    
@app.route("/", methods=['GET'])
def index():
    return "Welcome";
    
@app.route("/listeChantiers/", methods = ['GET'])
def ListeChantiers():
    global attribution
    return jsonify(attribution)
    
@app.route("/listeOuvriers/", methods = ['GET'])
def ListeOuvriers():
    global test
    return jsonify(test)
    
@app.route("/addOuvriers/", methods = ['GET'])
def addOuvrier():
    global test
    set_new_ouvrier("Jordan")
    return jsonify(test)
    

if __name__ == '__main__':
    app.run(debug=True)