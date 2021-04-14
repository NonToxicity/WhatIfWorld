import flask
from flask import request
import pandas as pd
from datetime import datetime as dt
import requests
from flask_cors import CORS, cross_origin


URL = "https://api.covid19api.com"
data = pd.read_csv('data.csv', names=['s', 'e', 'm']).set_index('m')

series = pd.Series(index=range(data.s.min(), dt.now().year + 1))
for m in data.index:
    series.loc[data.loc[m].s:data.loc[m].e] = m

app = flask.Flask(__name__)
cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:4200/"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET'])
@cross_origin()

def home():
    return "root"


@app.route('/countries')
def getCountries():
    countries = requests.get(URL + '/countries').json()
    return str(countries)

@app.route('/dayone')
def getDayOne():
    country = request.args.get('country', default='south-africa', type=str)
    dayone = requests.get(URL + '/dayone/country/' + country + '/status/' + 'confirmed').json()
    return str(dayone)

@app.route('/summary')
def getSummary():
    summary = requests.get(URL + '/summary').json()
    return str(summary)

@app.route('/statusbycountry')
def getstatus():
    country = request.args.get('country', default='south-africa', type=str)
    summary = requests.get(URL +'/country/'+country+'?from=2020-03-01T00:00:00Z&to=2020-04-01T00:00:00Z').json()
    return str(summary)

@app.route('/traveldatabycountry')
def getTravelData():
    country = request.args.get('country', default='south-africa', type=str)
    headers = {'X-Access-Token': '5cf9dfd5-3449-485e-b5ae-70a60e997864'}
    summary = requests.get(URL +'/premium/travel/country/'+country, headers=headers).json()
    return str(summary)


@app.route('/testsbycountry')
def getTestData():
    country = request.args.get('country', default='south-africa', type=str)
    headers = {'X-Access-Token': '5cf9dfd5-3449-485e-b5ae-70a60e997864'}
    summary = requests.get(URL +'/premium/country/testing/'+country, headers=headers).json()
    return str(summary)


@app.route('/whatifbycountry')
def getWhatIfByCountry():
    country = request.args.get('country', default='south-africa', type=str)
    date = request.args.get('date', default=1, type=int)
    handwash = request.args.get('handwash', default=1.0, type=float)
    restriction = request.args.get('restriction', default=0, type=int)
    cigarette = request.args.get('cigarette', default=0, type=float)
    return "[newCases:1689]"


@app.route('/register')
def register():
    username = request.args.get('username', type=str)
    password = request.args.get('password', type=str)
    return "[message: User Registered succesfully, status:200]"


@app.route('/login')
def login():
    username = request.args.get('username', type=str)
    password = request.args.get('password', type=str)
    return "[message: User Logged in succesfully, status:200]"

#if __name__ == '__main__':
#    app.run(debug=True)
