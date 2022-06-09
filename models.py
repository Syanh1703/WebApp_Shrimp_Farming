from flask import render_template, jsonify
from webapp import app
from data_collect import *

year_json = str(datetime.now().year)
day_json = str(datetime.now().day)
month_json = datetime.now().month
if month_json<10:
    month_json = str("0" + str(month_json))
else:
    month_json = str(month_json)
date_json = str(day + "-" + month_json)
print(f'date: {date_json}')

#Time
hour_json = datetime.now().hour
if hour_json<10:
    hour_json = str("0" + str(hour_json))
else:
    hour_json = str(hour_json)

minute_json = datetime.now().minute
if minute_json<10:
    minute_json = str("0" + str(minute_json))
else:
    minute_json = str(minute_json)

time_json = str(hour_json + ":" + minute_json) #Node datetime
print(f'time: {time_json}')

pH_array = MyNode("PH")
DO_array = MyNode("DO")
Temp_array = MyNode("T")

pH_hourly_data = MyNode("PH")
DO_hourly_data = MyNode("DO")
Temp_hourly_data = MyNode("T")

#Get latest data
Temp_array.get_latest_data()
DO_array.get_latest_data()
pH_array.get_latest_data()

#Get one hour data
Temp_hourly_data.get_hourly_val()
DO_hourly_data.get_hourly_val()
pH_hourly_data.get_hourly_val()

#Average value in one hour
avg_pH_val = 0.0
avg_DO_val = 0.0
avg_Temp_val = 0.0

avg_pH_one_hour_array = []
avg_DO_one_hour_array = []
avg_Temp_one_hour_array = []

#Daily array
avg_pH_daily_array = []
avg_DO_daily_array = []
avg_Temp_daily_array = []


def calculate_average_one_hour(original_lst, avg_lst,avg_val, avg_daily_array):
    for a in range(0,len(original_lst)):
        avg_lst.append(original_lst[a])
        if len(avg_lst) == 6: #Take the average value of 6 elements
            avg_val = round(sum(avg_lst)/len(avg_lst),3)
            avg_daily_array.append(avg_val)
            print(f'Daily value: {avg_daily_array}')
            print(f'len of daily value: {len(avg_daily_array)}')
            avg_lst = []

#calculate_average_one_hour(Temp_hourly_data.hourly_data, avg_Temp_one_hour_array, avg_Temp_val, avg_Temp_daily_array)
calculate_average_one_hour(DO_hourly_data.hourly_data, avg_DO_one_hour_array, avg_DO_val, avg_DO_daily_array)
calculate_average_one_hour(pH_hourly_data.hourly_data, avg_pH_one_hour_array, avg_pH_val, avg_pH_daily_array)

@app.route('/', methods=['POST', 'GET'])
def home():
    DO_val = DO_array.present_data[1]
    Temp_val = Temp_array.present_data[1]
    pH_val = pH_array.present_data[1]
    time = pH_array.present_data[2]

    calculate_average_one_hour(Temp_hourly_data.hourly_data, avg_Temp_one_hour_array, avg_Temp_val,
                               avg_Temp_daily_array)

    return render_template('sensors.html', PH = pH_val, DO = DO_val, Temp = Temp_val, date = time, Temp_axis = avg_Temp_daily_array, DO_axis = avg_DO_daily_array, PH_axis = avg_pH_daily_array)


@app.route("/test")
def test():
    return "WELCOME TO MY SITE!!!"

@app.route("/data_json")
def json():
    trial_data_set = [{
        "Node1":{
            year_json:{
                date_json:{
                    time_json:{
                        "PH": pH_array.present_data[1],
                        "DO": DO_array.present_data[1],
                        "T":Temp_array.present_data[1]
                    }
                }
            }
        }
    }]
    return jsonify(trial_data_set)

if __name__ == "__main__":
    app.run(debug=True)
