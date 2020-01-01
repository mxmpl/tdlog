from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

chantiers = [
{"start":"2020-01-05", "title":"Champs-sur-Marne", "ouvrier":"Max"},
{"start":"2020-01-08", "title":"Paris", "ouvrier":"Raph"},
{"start":"2020-01-10", "title":"Bordeaux", "ouvrier":"Margot"},
{"start":"2020-01-12", "title":"Noisy", "ouvrier":"Max2"}
]

@app.route("/", methods=['GET'])
def index():
    return "Welcome";

@app.route("/listeChantiers/", methods = ['GET'])
def ListeChantiers():
    global chantiers
    return jsonify(chantiers)

if __name__ == '__main__':
    app.run(debug=True)