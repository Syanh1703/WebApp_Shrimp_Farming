from pipes import Template
import sys
#Firebase Admin
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
import time

sys.path.insert(0, "..")

cred = credentials.Certificate('app.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://thesissensordatabase-de170-default-rtdb.firebaseio.com'
})
    
time_display = datetime.now()
time_str = time_display.strftime("%H:%M")
date_str = time_display.strftime("%Y-%d-%m")
date_display = str(date_str + "_" + time_str)
ref = db.reference("/Node1")

pH_ref = ref.child(str(date_display)).child("PH") #Get the key named pH
DO_ref = ref.child(str(date_display)).child("DO") #Get the key named DO
Temp_ref = ref.child(str(date_display)).child("T") #Get the key named Temperature

if __name__ == "__main__":
    # Put into time interval
    def minute_interval(min_before, min_after):
        if((min_after - min_before)>0): #Update per 5 min
            time_display = datetime.now()
            year_str = time_display.year
            time_str = time_display.strftime("%H:%M")
            date_str = time_display.strftime("%d-%m")
            ref_time = ref.child(str(year_str)).child(str(date_str))
            #Update data
            ref_time.update({
                str(time_str):
                {
                    "PH":"9",
                    "DO":"12",
                    "T": "34"
                }

            })
            print("Complete the update")

        else:
            print("Goodbye")
            
    while (True):
        min1 = datetime.now().minute
        print("min1 is :" + str(min1))

        time.sleep(60)  # Pause the process by 5 minute

        min2 = datetime.now().minute
        print("min2 is:" + str(min2))
        minute_interval(min1, min2)
    
        min1 = 0
        min2 = 0
        print("restart min to :" + str(min2))
        time.sleep(1)
        
