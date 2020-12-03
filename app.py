from flask import Flask, render_template, request
import requests
import json
import datetime
import pandas as pd
import re
import csv
import numpy as np
from scipy import spatial
import itertools

app = Flask(__name__)
@app.route('/')
def index():
    print("最初のページだよ")
    return render_template('index.html')

@app.route('/result', methods=['POST'])

def result():

    region = request.form.get('region')
    api_key = 'a09103f7f84acf2f773de5054185a05d'
    api = 'http://api.openweathermap.org/data/2.5/forecast?units=metric&q={city}&appid={key}'
    city_name = region
    url = api.format(city = city_name, key = api_key)
    response = requests.get(url)
    data = response.json()

    # 1. userの入力を受け取る・今日なのか明日なのか明後日なのか
    # ２いつの天気なのかを見てりすとのどのいんでっくすからでーたをとりだすか決める

    day = request.form.get('day')

    if day == "today":  
        temp = int(data['list'][1]['main']['temp'])
        humidity = int(data['list'][1]['main']['humidity'])
        weather = (data['list'][1]['weather'][0]['main'])
        keys = ["気温","湿度","天気"]
        values = [temp, humidity, weather]
        d = dict(zip(keys, values))
        todays_weather = d

    if day == "tomorrow":
        temp = int(data['list'][9]['main']['temp'])
        humidity = int(data['list'][9]['main']['humidity'])
        weather = (data['list'][9]['weather'][0]['main'])
        keys = ["気温","湿度","天気"]
        values = [temp, humidity, weather]
        d = dict(zip(keys, values))
        todays_weather = d

    if day == "day_after_tomorrow":
        temp = int(data['list'][17]['main']['temp'])
        humidity = int(data['list'][17]['main']['humidity'])
        weather = (data['list'][17]['weather'][0]['main'])
        keys = ["気温","湿度","天気"]
        values = [temp, humidity, weather]
        d = dict(zip(keys, values))
        todays_weather = d

    
    dates = []
    temp = []
    humidity = []
    items = []

    df = pd.read_csv("data_46.csv")

    for item in list(zip(df['main.temp'],df['main.humidity'])):
        items.append(list(item))
    
    b = np.array(list(itertools.chain.from_iterable([items])))
    a = np.array([[d["気温"],d["湿度"]]])
    tree = spatial.cKDTree(b)
    mindist, minid = tree.query(a)
    keys2 = ['temp','humidity']
    values2 = list(itertools.chain.from_iterable(b[minid]))
    d2 = dict(zip(keys2,values2))
    print(d2)

    filtered_df = df.query("`main.temp`=={0} & `main.humidity`=={1}".format(d2["temp"],d2["humidity"]),engine='python')
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
                with open("file_man{}.csv".format(item), "r") as ins:
                    for line in ins:
                        male_rows.append(line)
            except:
                print("cannot found csv.")
                pass
        print(male_rows)
        return render_template('result.html', message=message, urls=male_rows, weather=todays_weather)
    
    else:
        for item in list(set(dates)):
            try:
                with open("file{}.csv".format(item),"r") as ins:
                    for line in ins:
                        female_rows.append(line)

                    
            except:
                print("cannot found csv.")
                pass
        return render_template('result.html', message=message, urls=female_rows, weather=todays_weather )

app.run(host = '0.0.0.0',port=8080)