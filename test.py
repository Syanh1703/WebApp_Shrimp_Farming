from pipes import Template
import sys
#Firebase Admin
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import date, datetime
import time

#Rasp Library


sys.path.insert(0, "..")

cred = credentials.Certificate('app.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://thesissensordatabase-de170-default-rtdb.firebaseio.com'
})
    
time_display = datetime.now()
time_str = time_display.strftime("%H:%M")
date_str = time_display.strftime("%d-%m-%Y")

if __name__ == "__main__":

    #Set up the data set first
    ref = db.reference("/")
    ref.set({
        'Sensor':
            {
                'DO':
                    {
                        date_str:
                        {
                            'value': '35'
                        }
                    },
                'pH':
                    {
                        date_str:
                        {
                            'value': '10'
                        }
                    },
                'Temperature':
                    {
                        date_str:
                        {
                            'value': '3'
                        }
                    }
            }
    })

    # Put into time interval
    def minute_interval(min_before, min_after):
        if (min_after - min_before) >= 1:

            #Trial update the value
            ref = db.reference('Sensor')
            pH_ref = ref.child('pH').child(str(date_str)) #Get the key named pH
            DO_ref = ref.child('DO').child(str(date_str)) #Get the key named DO
            Temp_ref = ref.child('Temperature').child(str(date_str)) #Get the key named Temperature

            #Cretae a for loop for continuous update within 24 Hours
            for x in range(25):
                #Temperature
                Temp_value_index = str("value at " + str(x) + ":00")
                Temp_ref_dummy_value = 50 + int(x)
                Temp_ref.update({
                    str(Temp_value_index): Temp_ref_dummy_value
                })

                #DO
                DO_ref_value_index = str("value at " + str(x) + ":00")
                DO_ref_dummy_value = 60 + int(x)
                DO_ref.update({
                    str(DO_ref_value_index): DO_ref_dummy_value
                })

                #pH
                pH_ref_value_index = str("value at "+ str(x) + ":00")
                pH_ref_dummy_value = 80 + int(x)
                pH_ref.update({
                    str(pH_ref_value_index):pH_ref_dummy_value
                })
            #Restart the minute
            min_before = 0
            min_after = 0
            print("min_before is:" + str(min_before))
            print("min_after is: " + str(min_after))

        else:
            print("Goodbye")


    while 1:
        min1 = datetime.now().minute
        print("min1 is :" + str(min1))

        time.sleep(60)  # Pause the process by 1 minute

        min2 = datetime.now().minute
        print("min2 is :" + str(min2))

        minute_interval(min1, min2)
