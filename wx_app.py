#!/usr/bin python
import requests
import xml.etree.ElementTree as ET

# Create a string to query NOAA weather server
# Default is Addison, Dallas, and McKinney 
urlMETAR = 'https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=KADS%20KDAL%20KTKI&hoursBeforeNow=1'
urlTAF = 'https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=tafs&requestType=retrieve&format=xml&stationString=KADS%20KDAL%20KTKI&hoursBeforeNow=4'
rawResponse = requests.get(urlMETAR)
xmlContent = rawResponse.content
dataWX ={}
root = ET.fromstring(xmlContent)

for child in root:
    if child.tag == 'data':
        numResults = child.attrib['num_results']
        for report in child.iter('METAR'):
            print report[0].text
