# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 22:07:43 2021

@author: Satish Narasimhan
"""

Description
===========
This project / module has been built to determine the optimum angle of the solar panels for a given location. This is built usng Python.

The location can be provided as an postcode (UK, Canada), zip code (US) or city / area name (India, Rest of the world)

The output is spreadsheet generated with the values for the next 365 days, as a comma separated value (.csv) file in the downloads folder

Requirements
------------
Packages / pip installations required are:

solarenergy  - pip install solarenergy. Ref - https://github.com/MarcvdSluys/SolarEnergy
geocoder  - pip install geocoder. Ref - https://github.com/DenisCarriere/geocoder
from datetime => datetime
from dateutil.relativedelta => relativedelta
numpy
timezonefinder
pandas

Inputs to be provided for:
## Provide the location to obtain Latitude and Longitude of location in search string
loc = ''
filepath = ''
# Provide number of start date, days range for which the search is to be run
start_date = '2021-01-01'
Default date provided is 01st January 2021

Open cage API key
open_cage_api_key = ''


Example(s)
------------
In UK, just provide the post code against the location
e.g. 
loc = 'HA2 6PA'
In US, provide the zipcode or the locality
e.g.
loc = CA 92802
or 
loc = Anaheim, United States

For locations based in India or elsewhere, provide the city name or the locality
e.g.
loc = 'Bengaluru'
or loc = 'Jayanagar, Bengaluru'

