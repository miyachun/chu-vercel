from flask import Flask, render_template,request
import json,urllib.request
from itertools import zip_longest
import os
from http.server import BaseHTTPRequestHandler
from urllib import parse
import psycopg2

app = Flask(__name__)

url = os.environ.get('WEATHER_API')

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
upload_folder = os.path.join('static', 'uploads') 
app.config['UPLOAD'] = upload_folder
def get_db_connection():
    mydb = psycopg2.connect(
    host=os.environ.get("POSTGRES_HOST"),
    user=os.environ.get("POSTGRES_USER"),
    password=os.environ.get("POSTGRES_PASSWORD"),
    database=os.environ.get("POSTGRES_DATABASE"))
    return mydb



@app.route('/', methods=('GET', 'POST'))
def index():
    ansA=[]
    ansAll = {}
    Anscity = []
    Answx = []
    AnsmintT=[]
    AnsmaxtT = []
    ansCity=[]

    
    if request.method == 'POST':
        dropdownval = request.form.get('Gcity')
        data = urllib.request.urlopen(url).read()
        output = json.loads(data)
        location=output['records']['location']
        for i in location:
            city = i['locationName']
            if city==dropdownval:
                wx = i['weatherElement'][0]['time'][0]['parameter']['parameterName']
                maxtT = i['weatherElement'][4]['time'][0]['parameter']['parameterName']
                mintT = i['weatherElement'][2]['time'][0]['parameter']['parameterName']                
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
        Anscity.append(city0)
        Answx.append(wx0)
        AnsmaxtT.append(maxtT0)
        AnsmintT.append(mintT0)
        ansCity.append(city0)
    
    for elem1, elem2, elem3, elem4  in zip_longest(Anscity, Answx, AnsmintT, AnsmaxtT):
        ansAll.setdefault(elem1, []).append(elem2)
        ansAll.setdefault(elem1, []).append(elem3)
        ansAll.setdefault(elem1, []).append(elem4)  
   
    return render_template('index.html',ansAll=ansAll,ansA=ansA,ansCity=ansCity)

@app.route('/database')
def database():
    mydb = psycopg2.connect(
    host=os.environ.get("POSTGRES_HOST"),
    user=os.environ.get("POSTGRES_USER"),
    password=os.environ.get("POSTGRES_PASSWORD"),
    database=os.environ.get("POSTGRES_DATABASE"))

    mycursor = mydb.cursor()

    mydb.set_session(autocommit=True)






    a01 =mycursor.execute("SELECT * FROM abc")
    posts=a01.fetchall()
    return render_template('db.html', posts=a01)

    rows = cursor.fetchall()
    #mycursor.close()
    #mydb.close()
    return render_template('db.html',posts=mycursor.fetchall())


if __name__ == '__main__':
    app.run()
