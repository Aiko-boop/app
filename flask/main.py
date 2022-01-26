from sre_constants import IN_LOC_IGNORE
import  requests
import json
import numpy as np
import matplotlib.pyplot as plt


from flask import Flask,render_template,request
 
app = Flask(__name__)

VOICE_DIR = "voice_data"


@app.route('/')
def index():
    print("最初のページだよ")
    return render_template('index.html')

@app.route('/result', methods=['POST'])

def result():
    
    onsei_data = request.form.get('onsei_data')
    url = 'https://api.webempath.net/v2/analyzeWav'

    apikey = 'szp0hXz9kSl5LBEddf1ii6UnnJRFuXQ0130TmPUiJeg'
    payload = {'apikey':apikey}

    path = "C:/Users/aiko/Desktop/test/flask/voice_data/{}/無題.wav".format(onsei_data)
    wav = path 
    data = open(wav, 'rb')
    file = {'wav' : data}
    
    res = requests.post(url, params=payload, files=file)
    print(res.json())
    
        
    url2 = "https://ai-api.userlocal.jp/voice-emotion/basic-emotions" 

    with open(wav, 'rb') as voice: 
        response = requests.post(url2, files={"voice_data": voice})
        result = json.loads(response.content)
        print(result['emotion_detail'])
        label = ["angry","disgust","fear","happy","neutral","sad","surprise"]
        x = np.array([result['emotion_detail']['angry'],result['emotion_detail']['disgust'],
              result['emotion_detail']['fear'],result['emotion_detail']['happy'],
              result['emotion_detail']['neutral'],result['emotion_detail']['sad'],
              result['emotion_detail']['surprise']],)
        plt.pie(x, labels = label)
        emotions = plt.show()
         
         
    return render_template('result.html', result=res.json(),result2=emotions)


if __name__ == '__main__':
    app.debug = True
    app.run(host = 'localhost')











    
    
    

    


        