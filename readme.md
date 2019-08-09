# Cheapo Aviation Weather App
This is a lightweight aviation weather app to enable a user to quickly look up TAF and METAR information for flight planning purposes. It utilizes the ADDS XML API for up-to-date flight weather information. 

The Python Flask module will be used to develop the first iteration of this project. My long-term goal is to convert this to other platforms to expand my portfolio. 

## User Guide
Type in 4 letter ICAO identifier for any airports to find the METAR (current observation) and TAF (24 hr forecast). 

## Issues/Bugs
* Need to 'bleach' the input
* Make parseXML() and getWxRpt() methods more robust to prevent errors
* Add functionality so that users can omit the optional 'K' prefix for airports

## Disclaimer
This is being developed for personal use and academic purposes, but it not intended to replace certified flight planning software and tools. This application is not a substitute for the good judgement by the pilot-in-command and other flight crewmembers. 

## Design Notes
See the [Aviation Weather Center](https://www.aviationweather.gov/dataserver/example?datatype=metar) webpage for detailed information about their web API. 


