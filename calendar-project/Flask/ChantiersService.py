from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import  Api 

app = Flask(__name__)
CORS(app)

attribution = {"items":[
{"start":"2020-01-05", "chantier":"Champs-sur-Marn", "ouvrier":"Max"},
{"start":"2020-01-08", "chantier":"Paris", "ouvrier":"Raph"},
{"start":"2020-01-10", "chantier":"Bordeaux", "ouvrier":"Margot"},
{"start":"2020-01-08", "chantier":"Noisy", "ouvrier":"Max2"},
{"start":"2020-01-12", "chantier":"Mulhouse", "ouvrier":"Fredo", "end":"2020-01-15"}
]
}

test = { "totalItems":5,"items":[
{"start":"2020-01-05", "chantier":"Champs-sur-Marne", "ouvrier":"Max"},
{"start":"2020-01-08", "chantier":"Paris", "ouvrier":"Raph"},
{"start":"2020-01-10", "chantier":"Bordeaux", "ouvrier":"Margot"},
{"start":"2020-01-08", "chantier":"Noisy", "ouvrier":"Max2"},
{"start":"2020-01-12", "chantier":"Mulhouse", "ouvrier":"Fredo", "end":"2020-01-15"}
]
}


for dico in attribution["items"]:
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
    return jsonify(attribution["items"])
    
@app.route("/listeOuvriers/", methods = ['GET'])
def ListeOuvriers():
    global attribution
    return jsonify(attribution)
    
@app.route("/addOuvriers/", methods = ['POST'])
def addOuvrier():
	data = request.get_json()
	new_evenement = {"start":"2020-01-07", "title":data["nom"]+" est a Paris", "end":"2020-01-07", "ouvrier":data["nom"]}
	global attribution
	attribution["items"].append(new_evenement)
	return jsonify(attribution["items"])

if __name__ == '__main__':
    app.run(debug=True)