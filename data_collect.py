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

rounded_digits = 2

#Date
year = str(datetime.now().year)
day = str(datetime.now().day)
month = datetime.now().month
if month<10:
    month = str("0" + str(month))
    print(f'Smaller than 10: {month}')
else:
    month = str(month)
#date = str(day + "-" + month)
date = "1-07"
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
        self.year = year
        self.date = date
        self.time = 0
        self.avg = 0.0
        self.present_data = []
        self.pH_hourly_array = []
        self.DO_hourly_array = []
        self.Temp_hourly_array = []

    def get_latest_data(self):
        snapshot = db.reference('/Node1').child(year).child(date).order_by_key().limit_to_last(1).get()
        for key, val in snapshot.items():
            self.time = key
            self.present_data.append(self.sensorName)
            self.present_data.append(round(val[self.sensorName],rounded_digits))
            self.present_data.append(self.time)
            self.present_data.append(self.date)
            self.present_data.append(self.year)

    def get_online_chart(self):
        start = perf_counter()
        snapshot = db.reference('/Node1').child(year).child(date).order_by_key().limit_to_last(144).get()
        for key,val in snapshot.items():
            self.time = key
            self.pH_hourly_array.append(round(val['PH'], rounded_digits))
            self.DO_hourly_array.append(round(val['DO'], rounded_digits))
            self.Temp_hourly_array.append(round(val['T'], rounded_digits))

        finish = perf_counter()
        print(f'Value at {hour}:00')
        print(f'Running time: {finish-start}\n')


if __name__ == "__main__":
    pH_present = MyNode('PH')
    DO_present = MyNode('DO')
    Temp_present = MyNode('T')

    Temp_present.get_latest_data()
    pH_present.get_latest_data()
    DO_present.get_latest_data()

    pH_present.get_online_chart()
    DO_present.get_online_chart()
    Temp_present.get_online_chart()

    print(f'Temp hourly data is: {Temp_present.Temp_hourly_array}')
    print(f'DO hourly data is: {DO_present.DO_hourly_array}')
    print(f'PH hourly data: {pH_present.pH_hourly_array}')
    print(f'len: {len(pH_present.pH_hourly_array)}')

    print("")
    print(Temp_present.present_data)
    print(DO_present.present_data)
    print(pH_present.present_data)
    print(f'Taken time: {DO_present.present_data[2]}')
