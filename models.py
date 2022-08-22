from flask import render_template, jsonify
from webapp import app
from data_collect import *

sensor_list = ['PH', 'T', 'DO']
year_json = str(datetime.now().year)
month_json = datetime.now().month

if month_json < 10:
    month_json = str("0" + str(month_json))
else:
    month_json = str(month_json)
date_json = str(day + "-" + month_json)
#date_json = "2-08"
print(f'date: {date_json}')

# Time
hour_json = datetime.now().hour
if hour_json < 10:
    hour_json = str("0" + str(hour_json))
else:
    hour_json = str(hour_json)

minute_json = datetime.now().minute
if minute_json < 10:
    minute_json = str("0" + str(minute_json))
else:
    minute_json = str(minute_json)

time_json = str(hour_json + ":" + minute_json)  # Node datetime
print(f'time: {time_json}')


def calculate_average_one_hour(original_lst, avg_lst, avg_val, avg_daily_array):
    for a in range(0, len(original_lst)):
        avg_lst.append(original_lst[a])
        if len(avg_lst) == 6:  # Take the average value of 6 elements
            avg_val = round(sum(avg_lst) / len(avg_lst), 3)
            avg_daily_array.append(avg_val)
            print(f'Daily value: {avg_daily_array}')
            print(f'len of daily value: {len(avg_daily_array)}')
            avg_lst = []


def call_api_each_sensor(name, position_in_list):
    global year, date, time
    present_array = []
    for sensor_id in sensor_list:
        sensor_node = MyNode(sensor_id)
        sensor_node.get_latest_data()
        temp_array = sensor_node.present_data
        time = temp_array[2]
        date = temp_array[3]
        year = temp_array[4]
        present_array.append(temp_array[1])
    print(f' The time is: {time}')
    sensor_data_set = [{
        "id": name,
        "date": date,
        "time": time,
        "year": year,
        "value": present_array[position_in_list]
    }]
    print(f'The {name} data set is {sensor_data_set}')
    sensor_api = jsonify(sensor_data_set)
    return sensor_api


@app.route('/', methods=['POST', 'GET'])
def home():
    start = perf_counter()
    present_array = []
    pH_hourly_array = []
    DO_hourly_array = []
    Temp_hourly_array = []
    time_measured = "0"
    year_taken = "0"
    date_taken = "0"

    # Daily array
    avg_pH_daily_array = []
    avg_DO_daily_array = []
    avg_Temp_daily_array = []

    avg_pH_one_hour_array = []
    avg_DO_one_hour_array = []
    avg_Temp_one_hour_array = []

    # Average value in one hour
    avg_pH_val = 0.0
    avg_DO_val = 0.0
    avg_Temp_val = 0.0

    for sensor_id in sensor_list:
        sensor_node = MyNode(sensor_id)
        sensor_node_2 = MyNode(sensor_id)

        sensor_node.get_latest_data()
        temp_array = sensor_node.present_data
        present_array.append(temp_array[1])
        time_measured = temp_array[2]
        date_taken = temp_array[3]
        year_taken = temp_array[4]

        sensor_node_2.get_online_chart()
        pH_hourly_array = sensor_node_2.pH_hourly_array
        DO_hourly_array = sensor_node_2.DO_hourly_array
        Temp_hourly_array = sensor_node_2.Temp_hourly_array

    calculate_average_one_hour(Temp_hourly_array, avg_Temp_one_hour_array, avg_Temp_val,
                               avg_Temp_daily_array)
    calculate_average_one_hour(DO_hourly_array, avg_DO_one_hour_array, avg_DO_val, avg_DO_daily_array)
    calculate_average_one_hour(pH_hourly_array, avg_pH_one_hour_array, avg_pH_val, avg_pH_daily_array)

    data_set = [{
        "id": 1,
        "year": year_taken,
        "date": date_taken,
        "timeTaken": time_measured,
        "PH": present_array[0],
        "DO": present_array[2],
        "T": present_array[1],
    }]
    datas = jsonify(data_set)
    finish = perf_counter()
    print(f'Run time is:{finish-start}')

    return render_template('sensors.html', PH=present_array[0], DO=present_array[2],
                           Temp=present_array[1], date=date_taken,
                           Temp_axis=avg_Temp_daily_array,
                           DO_axis=avg_DO_daily_array, PH_axis=avg_pH_daily_array, timeMeasured=time_measured,
                           datas=datas.json)


@app.route('/intro')
def test():
    return "WELCOME TO MY SITE!!!"

@app.route('/PH', methods=['POST', 'GET'])
def pH_get():
    return call_api_each_sensor("PH", 0)

@app.route('/DO', methods = ['POST' , 'GET'])
def DO_get():
    return call_api_each_sensor("DO", 2)

@app.route('/Temp', methods = ['POST', 'GET'])
def Temp_get():
    return call_api_each_sensor("Temp", 1)

if __name__ == "__main__":
    app.run(debug=True)
