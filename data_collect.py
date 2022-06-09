import sys
from time import perf_counter

# Firebase Admin
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

sys.path.insert(0, "..")

cred = credentials.Certificate('app.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://thesissensordatabase-de170-default-rtdb.firebaseio.com'
})

#Date
year = str(datetime.now().year)
day = str(datetime.now().day)
month = datetime.now().month
if month<10:
    month = str("0" + str(month))
    print(f'Smaller than 10: {month}')
else:
    month = str(month)
date = str(day + "-" + month)
print(f'{date}')

#Time
hour = datetime.now().hour
if hour<10:
    hour = str("0" + str(hour))
else:
    hour = str(hour)

minute = datetime.now().minute
if minute<10:
    minute = str("0" + str(minute))
else:
    minute = str(minute)
time = str(hour + ":" + minute) #Node datetime
print(f'time: {time}')

class MyNode():

    #a dict to store data
    def __init__(self, sensorName):
        self.node_name = '/Node1'
        self.sensorName = sensorName
        self.year = 0
        self.date = 0
        self.time = 0
        self.avg = 0.0
        self.present_data = []
        self.hourly_data = []
        self.daily_data = []

    def round_value(self):
        return round(self,2)

    def get_latest_data(self):
        snapshot = db.reference('/Node1').child(year).child(date).order_by_key().limit_to_last(1).get()
        for key, val in snapshot.items():
            self.time = key
            self.present_data.append(self.sensorName)
            self.present_data.append(round(val[self.sensorName],2))
            self.present_data.append(self.time)

    def get_hourly_val(self):
        start = perf_counter()
        # for x in range(0,60):
        #     if x<10:
        #         snapshot = db.reference('/Node1').child(year).child(date).child("time_" + str(hour) + ":0" + str(x)).child(
        #             self.sensorName)
        #         if snapshot.get() is not None:
        #             self.hourly_data.append(snapshot.get())
        #     else:
        #         snapshot = db.reference('/Node1').child(year).child(date).child("time_" + "19" + ":" + str(x)).child(self.sensorName)
        #         if snapshot.get() is not None:
        #             self.hourly_data.append(snapshot.get())

        snapshot = db.reference('/Node1').child(year).child(date).order_by_key().limit_to_last(144).get()
        for key,val in snapshot.items():
            self.time = key
            self.hourly_data.append(round(val[self.sensorName], 2))

        finish = perf_counter()
        print(f'Value at {hour} ')
        print(f'Running time: {finish-start}')

    def get_name(self):
        return self.sensorName

    def call_api(self):
        pass

if __name__ == "__main__":
    pH_present = MyNode('PH')
    DO_present = MyNode('DO')
    Temp_present = MyNode('T')

    Temp_present.get_latest_data()
    pH_present.get_latest_data()
    DO_present.get_latest_data()

    pH_present.get_hourly_val()
    DO_present.get_hourly_val()
    Temp_present.get_hourly_val()

    print(f'Temp hourly data is: {Temp_present.hourly_data}')
    print(f'DO hourly data is: {DO_present.hourly_data}')
    print(f'PH hourly data: {pH_present.hourly_data}')
    print(f'len: {len(pH_present.hourly_data)}')

    print(Temp_present.present_data)
    print(DO_present.present_data)
    print(pH_present.present_data)
