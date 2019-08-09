#!/usr/bin python
import requests, re, os, sys, string
import xml.etree.ElementTree as ET

from flask import Flask, render_template, request, 
    redirect, jsonify, url_for, flash

from flask import session as login_session
from flask import make_response

# Create a string to query NOAA weather server
# Default is Addison, Dallas, and McKinney 

metarString = ' kads  f46 '
tafString = 'kdal kftw'

app = Flask(__name__)
APPLICATION_NAME = "Cheapo Weather App"


def processString(inputString):
    # alternative to use Javascript for input validation
    return re.sub(" +", '%20', inputString)

def getWxRpt(metarString, tafString):
    urlMETAR = 'https://www.aviationweather.gov/adds/dataserver_current/\
        httpparam?dataSource=metars&requestType=retrieve&\
        format=xml&stationString={0}&hoursBeforeNow=1'.format(metarString)
    urlTAF = 'https://www.aviationweather.gov/adds/dataserver_current/\
        httpparam?dataSource=tafs&requestType=retrieve&\
        format=xml&stationString={0}&hoursBeforeNow=4'.format(tafString)
    rawResponse = requests.get(urlMETAR)
    xmlContent = rawResponse.content
    dataMETAR = {}
    dataTAF = {}
    root = ET.fromstring(xmlContent)

    for child in root :
        if child.tag == 'data' :
            numResults = child.attrib['num_results']
            if num_results == 0 :
                dataMETAR['No data found'] = 'Please try another query'
            for report in child.iter('METAR') :
                if report[0].text :
                    dataMETAR[report[1].text] = report[0].text
                else :
                    # If blank data found, will display an error
                    # Redesign with a Try/Except statement
                    # Examine XML format for a bad query result
                    dataMETAR[report[1].text] = report[1].text + \
                        "No data available or no data found for this station"
    return  dataMETAR.values(), dataTAF.values()

metarString = processString(metarString)
#print getWxRpt(metarString, tafString)

@app.route('/', methods=['GET'])
def showMainPage():
    return render_template('mainpage.html')

@app.route('/', methods=['POST'])
def getWeatherData():
    print form.inputString.data
# Example for redirects
# redirect(url_for('methodName', arguments...))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)