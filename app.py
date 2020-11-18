from flask import Flask, render_template, request
import requests
import json
import datetime
import pandas as pd
import re
import csv

app = Flask(__name__)
@app.route('/')
def index():
    print("最初のページだよ")
    return render_template('index.html')

@app.route('/result', methods=['POST'])

def result():

    region = request.form.get('region')
    api_key = 'a09103f7f84acf2f773de5054185a05d'
    api = 'http://api.openweathermap.org/data/2.5/forecast?units=metric&q={city}&APPID={key}&cnt={limit}'
    city_name = region
    request_line = 1
    url = api.format(city = city_name, key = api_key, limit = request_line)
    response = requests.get(url)
    data = response.json()

    for i in data['list']:
        temp = int(i['main']['temp'])
        humidity = int(i['main']['humidity'])
        weather = (i['weather'][0]['main'])
        keys = ["気温","湿度","天気"]
        values = [temp, humidity, weather]
        d = dict(zip(keys, values))
        todays_weather = d
    
    dates = []

    df = pd.read_csv("data_46.csv")
    filtered_df = df.query("{0}-3<=`main.temp`<={0}+3 & {1}-3<=`main.humidity`<={1}+3".format(d["temp"],d["humidity"]),engine='numexpr')
    for u in filtered_df['dt_iso']:
        result = re.search(r"[0-9]{4}-[0-9]{2}-[0-9]{2}",u)
        date = str(result.group().replace('-',''))
        dates.append(date)
    print(list(set(dates)))

    male_rows = []
    female_rows = []
    name = request.form.get('name')
    message = name

    gender = request.form.get('gender')
    if gender == "male":
        for item in list(set(dates)):
            try:
                with open("file_man{}.csv".format(item)) as f:
                    reader = csv.reader(f)
                    for row in reader:
                        male_rows.append(row)
            except:
                print("cannot found csv.")
                pass

        return render_template('result.html', message=message, urls=male_rows, weather=todays_weather)
    
    else:
        for item in list(set(dates)):
            try:
                with open("file{}.csv".format(item)) as f:
                    reader = csv.reader(f)
                    for row in reader:
                        female_rows.append(row)
            except:
                print("cannot found csv.")
                pass
        return render_template('result.html', message=message, urls=female_rows, weather=todays_weather )

app.run(host = '0.0.0.0',port=8080)