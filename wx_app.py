#!/usr/bin python
import requests, re, os, sys, string, bleach
import xml.etree.ElementTree as ET

from flask import Flask, render_template, request, \
    redirect, jsonify, url_for, flash

from flask import session as login_session
from flask import make_response

from requests import RequestException, ConnectionError, ReadTimeout, Timeout, TooManyRedirects, HTTPError

app = Flask(__name__)
APPLICATION_NAME = "Cheapo Weather App"


def processString(inputString):
    # alternative to use Javascript for input validation
    return re.sub(' +', '%20', inputString)

def getWxRpt(metarString, tafString):
    urlMETAR = 'https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString={0}&hoursBeforeNow=1'.format(metarString)
    urlTAF = 'https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=tafs&requestType=retrieve&format=xml&stationString={0}&hoursBeforeNow=4'.format(tafString)
    try:    
        rawResponse = requests.get(urlMETAR, timeout=(2,5), verify=True)
        xmlContent = rawResponse.content
        rootMETAR = ET.fromstring(xmlContent)
    except (RequestException, ConnectionError, ReadTimeout, Timeout, TooManyRedirects, HTTPError) as error:
        print error
        dataMETAR = ['No METAR Data available' + error]

    try:
        typeRpt = str(rootMETAR[6][0].tag)
        dataMETAR = parseXML(rootMETAR)
    except IndexError:
        print 'IndexError occured for METAR request' + metarString 
        dataMETAR = ['No METAR Data available']
    try:
        rawResponse = requests.get(urlTAF, timeout=(2,5), verify=True)
        xmlContent = rawResponse.content
        rootTAF = ET.fromstring(xmlContent)
    except (RequestException, ConnectionError, ReadTimeout, Timeout, TooManyRedirects, HTTPError) as error:
        print error
        dataTAF = ['No TAF Data available' + error]
    try:
        typeRpt = str(rootTAF[6][0].tag)
        dataTAF = parseXML(rootTAF)
    except IndexError:
        print 'IndexError occured for TAF request' + tafString 
        dataTAF = ['No TAF Data available']
    return dataMETAR, dataTAF

def parseXML(root):
    data = {}
    numResults = 0
    for child in root:
        if child.tag == 'data' :
            numResults = child.attrib['num_results']
            if not numResults :
                data['No data found'] = 'Please try another query'
            else:
                for report in child.iter(str(root[6][0].tag)) :
                    if report[0].text :
                        data[report[1].text] = report[0].text
                    else :
                        # If blank data found, will display an error
                        # Redesign with a Try/Except statement
                        # Examine XML format for a bad query result
                        data[report[1].text] = report[1].text + \
                            "No data available or no data found for this station"
    return data.values()

@app.route('/', methods=['GET', 'POST'])
def showMainPage():
    results = []
    if request.method == 'POST':
        sanitizedString = bleach.clean(request.form['inputString'])
        results = getWxRpt(processString(sanitizedString),
            processString(sanitizedString))
        return render_template('reports.html', results=results)
    return render_template('mainpage.html', results=results)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)