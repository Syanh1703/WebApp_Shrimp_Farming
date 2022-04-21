
from dataclasses import dataclass
import sys
from time import time
from unicodedata import name

#Firebase Admin
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

#Flask
from flask import Flask, redirect, render_template, url_for, jsonify
from sqlalchemy import true

sys.path.insert(0, "..")


cred = credentials.Certificate('app.json')
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://thesissensordatabase-de170-default-rtdb.firebaseio.com'
})

#Put into the web app
app = Flask(__name__)

@app.route('/data_json')
def data_json():
    time_display = datetime.now()
    time_str = time_display.strftime("%H:%M")
    date_str = time_display.strftime("%d-%m-%Y")

    # Get data from Firebase
    ref_pH = db.reference('/Sensor/pH/' + str(date_str) + '/value')
    ref_DO = db.reference('/Sensor/DO/' + str(date_str) + '/value')
    ref_Temp= db.reference('/Sensor/Temperature/' + str(date_str) + '/value')

    #Convert to float 
    float_pH = float(ref_pH.get())
    float_DO = float(ref_DO.get())
    float_Temp = float(ref_Temp.get())    
   
    sensor_data=[
        {
            "id": 0,
            "name": "DO",
            "value": float_DO,
            "date": date_str,
            "time": time_str
        },

        {
            "id": 1,
            "name": "Temperature",
            "value": float_Temp,
            "date": date_str,
            "time": time_str
        },

        {
            "id" :2,
            "name": "pH",
            "value": float_pH,
            "date": date_str,
            "time": time_str
        }
    ]
    return jsonify(sensor_data)

@app.route('/', methods=['POST', 'GET'])
def index():
    #Get jsonified data
    sensor_data = data_json()
    return render_template('sensors.html', 
    data=sensor_data.json)


if __name__=="__main__":
    app.run(debug=True)
    def minute_interval(min_before, min_after):
        if (true):
            min_before = 0
            min_after = 0
            print("min_before is:" + str(min_before))
            print("min_after is: " + str(min_after))
            index()
        else:
            print("Goodbye")

      