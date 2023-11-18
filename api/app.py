from flask import Flask, render_template,redirect, request

import json,urllib.request
from itertools import zip_longest
import os
app = Flask(__name__)

url = os.environ.get('WEATHER_API')

@app.route('/', methods=('GET', 'POST'))
def index():
    ansA=[]
    ansAll = {}
    Anscity = []
    Answx = []
    AnsmintT=[]
    AnsmaxtT = []
    ansCity=[]
    
    ci=[]
    
    if request.method == 'POST':
        dropdownval = request.form.get('Gcity')
        #print(dropdownval)  
        data = urllib.request.urlopen(url).read()
        output = json.loads(data)
        location=output['records']['location']
        for i in location:
            city = i['locationName']
            if city==dropdownval:
                wx = i['weatherElement'][0]['time'][0]['parameter']['parameterName']
                maxtT = i['weatherElement'][4]['time'][0]['parameter']['parameterName']
                mintT = i['weatherElement'][2]['time'][0]['parameter']['parameterName']
                ci = i['weatherElement'][3]['time'][0]['parameter']['parameterName']
                pop = i['weatherElement'][4]['time'][0]['parameter']['parameterName']
                #print(f'{city}未來 8 小時{wx}，最高溫 {maxtT} 度，最低溫 {mintT} 度，降雨機率 {pop} %')
                ansA.append(city)
                ansA.append(wx)
                ansA.append(mintT)
                ansA.append(maxtT)             
                
    
        render_template('index.html',ansAll=ansAll,ansA=ansA,ansCity=ansCity)
 
       
    data = urllib.request.urlopen(url).read()
    output = json.loads(data)
    location=output['records']['location']
        
    for i in location:
        city0 = i['locationName'] 
        wx0 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']
        maxtT0 = i['weatherElement'][4]['time'][0]['parameter']['parameterName']
        mintT0 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']
        #ci0 = i['weatherElement'][3]['time'][0]['parameter']['parameterName']
        #pop0 = i['weatherElement'][4]['time'][0]['parameter']['parameterName']    
        #print(mintT0)
        Anscity.append(city0)
        Answx.append(wx0)
        AnsmaxtT.append(maxtT0)
        AnsmintT.append(mintT0)
        ansCity.append(city0)
        #ci.append(ci0)

    
    for elem1, elem2, elem3, elem4  in zip_longest(Anscity, Answx, AnsmintT, AnsmaxtT):
        ansAll.setdefault(elem1, []).append(elem2)
        ansAll.setdefault(elem1, []).append(elem3)
        ansAll.setdefault(elem1, []).append(elem4)      
        
 
    
            
    #print(ansAll)
    return render_template('index.html',ansAll=ansAll,ansA=ansA,ansCity=ansCity)



if __name__ == '__main__':
    app.run()
