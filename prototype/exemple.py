from flask import Flask
from flask import request
from flask import render_template
import csv 


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/', methods=['POST'])
def text_box():
    text = request.form['text']
    
    with open("chantiers.csv", mode = "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow([text])
    processed_text = text.upper()
    return render_template("bienvenue.html" , message = processed_text )

if __name__ == '__main__':
    app.run()

