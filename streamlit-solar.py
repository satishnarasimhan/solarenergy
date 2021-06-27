# -*- coding: utf-8 -*-
"""
Created on Tue May 25 14:13:52 2021

@author: Satish Narasimhan
"""

import solarenergy as se
import geocoder
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import timezonefinder
import pandas as pd
import streamlit as st

def getDaysList(start_date, td):
    dates = []
    dt = datetime.strptime(start_date, "%Y-%m-%d")
    
    for n in range(0, td):
        dates.append(
            (dt + relativedelta(days=n)).strftime('%Y-%m-%d'))
    return dates

def user_input():

    data = {'Location': loc
            ,'No. of days': dt}
    inputs = pd.DataFrame(data, index=[0])
    return inputs

## Provide the location to obtain Latitude and Longitude of location in search string
open_cage_api_key = '<<>>'

# Streamlit inputs

st.write("""

# Solar Energy Maximiser!

""")

st.sidebar.header('User Input Values')
dt = st.sidebar.slider('Number of days - between 1 and 366', 1, 366, 1)

loc = st.sidebar.text_input('Please input the location', 'Bengaluru')


df = user_input()

st.subheader('User Entered details are')
st.write(df)


g = geocoder.opencage( loc , key = open_cage_api_key)
 
coord = g.latlng

city = g.city

lat = (round(g.latlng[0],4))
lon = (round(g.latlng[1],4))

# Provide number of date range for which the search is to be run. 
# Default start date will be current date
day = datetime.now()
today = day.strftime("%Y-%m-%d")
#day = today#"16-06-2021"
start_date = today #'2021-01-01'
# Generate the list of days for which the dataframe is to be generated
datelist = getDaysList(start_date, dt)

# Orientation of the solar panels:
# Azimuth ('wind direction') of my panels are facing.  Note: South=0, W=90° (pi/2 rad) in the northern hemisphere!  (rad). Face south in the northern hemisphere
spAz   = -0*se.d2r 
# Inclination of my panels w.r.t. the horizontal  (rad). Keeping the value the same as Earth's tilt
spIncl = 23.4*se.d2r  

# Geographical location of the solar panels:
geoLon = lon*se.d2r  # Geographic longitude (>0 for eastern hemisphere; ° -> rad)
geoLat = lat*se.d2r  # Geographic latitude  (>0 for northern hemisphere; ° -> rad)

## Obtain the timezone for the given location
tf = timezonefinder.TimezoneFinder()
myTZ = str(tf.certain_timezone_at(lat=geoLat, lng=geoLon))
#print(myTZ)

# Define columns of the dataframe
column_names = ["Date","Time (hrs)","Sun Az°","Sun Altitude°","Sun Distance AU","Sun-panels angle°","Solar constant W/m²","Air Mass","Ext. Factor","Ext. Radiation W/m²","DNI (clear sky) W/m²", "Direct Insolation W/m²"]

df_result = pd.DataFrame(columns = column_names)

# Hour of the day for which the solar panel angle is to be calculated
# Default is 12 i.e 12 noon
h = 12

for d in datelist:
    datee = datetime.strptime(d, "%Y-%m-%d")
    year = datee.year
    month = datee.month
    day = datee.day
# Compute Sun position (uses SolTrack from Solarenergy behind the scenes):
    sunAz,sunAlt,sunDist = se.sun_position_from_date_and_time(geoLon,geoLat, year,month,day, h, timezone=myTZ)
    
    AM        = se.airmass(sunAlt)                               # Air mass for this Sun altitude
    extFac    = se.extinction_factor(AM)                          # Extinction factor at sea level for this airmass
    cosTheta  = se.cos_angle_sun_panels(spAz,spIncl, sunAz,sunAlt)  # cos of the angle with which Sun hits my panels
    theta     = np.arccos(cosTheta)                              # Angle with which Sun hits my panels
    
    Iext      = se.solConst / sunDist**2                         # Extraterrestrial radiation = Solar constant, scaled with distance
    DNIcs     = Iext / extFac                                    # DNI for a clear sky
    dirRad    = DNIcs * cosTheta                                 # Insolation of direct sunlight on my panels
    
    df_result = df_result.append({"Date": d, "Time (hrs)": h, "Sun Az°": (sunAz*se.r2d), "Sun Altitude°" :  (sunAlt*se.r2d), "Sun Distance AU" : (sunDist), "Sun-panels angle°" : (theta*se.r2d),"Solar constant W/m²" : (se.solConst) ,"Air Mass" : (AM), "Ext. Factor" :  (extFac), "Ext. Radiation W/m²" : (Iext), "DNI (clear sky) W/m²": (DNIcs), "Direct Insolation W/m²": (dirRad)},ignore_index=True)
        
res = df_result.head(10)
st.subheader('Summary of the results')
st.write(res)

# Minimum value of Sun Panels angle
st.subheader('Minimum value of sun panels angle w.r.t. the horizontal')
mini = (df_result[(df_result['Sun-panels angle°'] == df_result['Sun-panels angle°'].min())])
st.write((mini['Sun-panels angle°'].values[0]))

st.subheader('Maximum value of Sun Panels angle w.r.t. the horizontal')
maxi = (df_result[(df_result['Sun-panels angle°'] == df_result['Sun-panels angle°'].max())])
st.write((maxi['Sun-panels angle°'].values[0]))

