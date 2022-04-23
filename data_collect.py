
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
from flask import Flask, redirect, render_template, jsonify
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
    ref = db.reference('Sensor')
    pH_ref = ref.child('pH').child(str(date_str)).child('value') #Get the key named pH
    DO_ref = ref.child('DO').child(str(date_str)).child('value') #Get the key named DO
    Temp_ref = ref.child('Temperature').child(str(date_str)).child('value') #Get the key named Temperature

    #Convert to string 
    str_pH = str(pH_ref.get())
    str_DO = str(DO_ref.get())
    str_Temp = str(Temp_ref.get()) 

    #Data set for the present value
    sensor_data=[
        {
            "id": 0,
            "name": "DO",
            "value": str_DO,
            "date": date_str,
            "time": time_str
        },

        {
            "id": 1,
            "name": "Temperature",
            "value": str_Temp,
            "date": date_str,
            "time": time_str
        },

        {
            "id" :2,    
            "name": "pH",
            "value": str_pH,
            "date": date_str,
            "time": time_str
        }
    ]
    return jsonify(sensor_data)  

@app.route('/hourly_data_json')
def hourly_data_json():
    
    time_display = datetime.now()

    date_str = time_display.strftime("%d-%m-%Y")

    # Get data from Firebase
    ref = db.reference('Sensor')
    pH_ref = ref.child('pH').child(str(date_str)).child('value') #Get the key named pH
    DO_ref = ref.child('DO').child(str(date_str)).child('value') #Get the key named DO
    Temp_ref = ref.child('Temperature').child(str(date_str)).child('value') #Get the key named Temperature

    #Convert to string 
    str_pH = str(pH_ref.get())
    str_DO = str(DO_ref.get())
    str_Temp = str(Temp_ref.get())  

    #hourly_value = str("value at "+ str(x) + ":00")
    hourly_set = [
        {
            "id": 3,
            "hour": 0,
            "value": str_DO
        },
        {
            "id": 4,
            "hour": 0,
            "value":str_Temp
        },
        {
            "id": 5,
            "hour": 0,
            "value":str_pH
        }
    ]
    return jsonify(hourly_set)  

@app.route('/', methods=['POST', 'GET'])
def index():
    #Get jsonified data
    sensor_data = data_json()
    hourly_set = hourly_data_json()
    return render_template('sensors.html', 
    data=sensor_data.json, hourly_array=hourly_set.json)

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

      