from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import  Api 

app = Flask(__name__)
CORS(app)

attribution = [
{"start":"2020-01-05", "chantier":"Champs-sur-Marn", "ouvrier":"Max"},
{"start":"2020-01-08", "chantier":"Paris", "ouvrier":"Raph"},
{"start":"2020-01-10", "chantier":"Bordeaux", "ouvrier":"Margot"},
{"start":"2020-01-08", "chantier":"Noisy", "ouvrier":"Max2"},
{"start":"2020-01-12", "chantier":"Mulhouse", "ouvrier":"Fredo", "end":"2020-01-15"}
]

ouvriers = [
{"id":"0", "name":"Max", "chantiers":[{"id":"1","name":"paris"}]},
{"id":"1", "name":"Raph"},
{"id":"2", "name":"Margot"},
{"id":"3", "name":"Max2"},
{"id":"4", "name":"Fredo"},
]

for dico in attribution:
    dico["title"] = dico["ouvrier"] + " est a " + dico["chantier"]
    
# def set_new_ouvrier(ouvrier):
#     global ouvriers 
#     ouvriers.append({"ouvrier":ouvrier})
    
@app.route("/", methods=['GET'])
def index():
    return "Welcome"
    
@app.route("/listeChantiers/", methods = ['GET'])
def ListeChantiers():
    global attribution
    return jsonify(attribution)

@app.route("/listeOuvriers/", methods = ['GET', 'POST', 'DELETE', 'PUT'])
def ListeOuvriers():
    global ouvriers
    print("liste",ouvriers)
    data = request.get_json()
    
    if (request.method == "POST"):
        lastId = int(ouvriers[-1]["id"])
        ouvriers.append({"id":str(lastId + 1), "name": data["name"]})
        
    return jsonify(ouvriers)
 
@app.route("/listeOuvriers/<id>", methods = ['GET', 'POST', 'DELETE', 'PUT'])
def OuvrierId(id):
    global ouvriers
    
    if (request.method == "GET"):
        for ouvrier in ouvriers:
            if ouvrier["id"] == id:
                return jsonify(ouvrier)
                
    elif (request.method == "PUT"):
        data = request.get_json()
        for ouvrier in ouvriers:
            if ouvrier["id"] == id:
                ouvrier["name"] = data["name"]

    elif (request.method == "DELETE"):
        del ouvriers[int(id)]
        
    return jsonify(ouvriers)

@app.route("/addOuvriers/", methods = ['POST'])
def addOuvrier():
	data = request.get_json()
	new_evenement = {"start":"2020-01-07", "title":data["nom"]+" est a Paris", "end":"2020-01-07"}
	global attribution
	attribution.append(new_evenement)
	return jsonify(attribution)

if __name__ == '__main__':
    app.run(debug=True)