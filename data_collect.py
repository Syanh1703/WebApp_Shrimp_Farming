import sys
from time import perf_counter

# Firebase Admin
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

# Flask
from flask import Flask, render_template, jsonify

sys.path.insert(0, "..")

cred = credentials.Certificate('app.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://thesissensordatabase-de170-default-rtdb.firebaseio.com'
})

class MyNode():

    #a dict to store data
    def __init__(self, sensorName):
        self.sensorName = sensorName
        self.year = 0
        self.date = 0
        self.hour = 0
        self.minute = 0
        self.avg = 0.0
        self.pH_array_hourly = []
        self.DO_array_hourly = []
        self.Temp_array_hourly = []
        self.pH_array_daily = []
        self.DO_array_daily = []
        self.Temp_array_daily = []

    def call_api(self):
        pass

if __name__ == "__main__":
    print("hello")
