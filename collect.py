import sys

#Firebase Admin
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

#Flask
from flask import Flask


sys.path.insert(0, "..")


cred = credentials.Certificate('app.json')
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://thesissensordatabase-de170-default-rtdb.firebaseio.com'
})

# Get data
ref1 = db.reference('/Sensor/H20/')
ref2 = db.reference('/value/pH')
ref3 = db.reference('value/DO')
ref4 = db.reference('value/Temp')

print(ref1.get())
val_pH = print(round(ref2.get(), 2))
val_DO = print(round(ref3.get(),2))
val_Temp = print(round(ref4.get(),2))

#Put into the web app
app = Flask(__name__)

@app.route("/")
def index():
    return "The value of DO is: " + val_DO