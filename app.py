from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("theory.cpe.ku.ac.th", username = "user07", password = "pass07")
db = client.db07

def get_temperatures():
    temperatures = db.temperatures
    return list(temperatures.find())

def cal_diff(temps):
    old_temp = temps[0]['t']
    for item in temps:
        item['diff'] = item['t'] - old_temp
        old_temp = item['t']

@app.route("/")
def index():
    temperatures = get_temperatures()
    if len(temperatures) > 0:
        cal_diff(temperatures)

    return render_template("index.html",
        temperatures=temperatures
    )

@app.route("/tempform", methods=['GET','POST'])
def temp_form():
    if request.method == 'POST':
        try:
            t = float(request.form['t'])
            temperatures = db.temperatures
            temperatures.insert_one({'t': t })
            return redirect("/")
        except ValueError:
            return redirect("/")     
    return render_template("tempform.html")


app.run(debug=True, port=8000)