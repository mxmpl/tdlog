from flask import Flask
from flask import request
from flask import render_template
# import pandas


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/', methods=['POST'])
def text_box():
    text = request.form['text']
    
    with open('chantiers.csv','a') as open_csv:
    	open_csv.write(text)
   	# Fonctionne pas mais pourra servir dans un deuxieme temps
    # df = pandas.read_csv('chantiers.csv')
    # df.append([text])
    # df.to_csv("chantiers.csv", sep=',', encoding='utf-8')
    processed_text = text.upper()
    return render_template("bienvenue.html" , message = processed_text )

if __name__ == '__main__':
    app.run()

