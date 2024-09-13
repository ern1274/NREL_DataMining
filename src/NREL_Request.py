"""
File: NREL_Request.py
Description: A program that performs Extract, Transform and Load operations
            on solar data from NREL and calls functions to analyze
            data using data mining methods
Language: Python 3.8
Author: Ethan Ray Nunez     ern1274@rit.edu
"""

from NREL_DataMining.src import config
import os
import ctypes
import pandas as pd
import http.client, urllib.parse
import json

url = "https://developer.nrel.gov/api/nsrdb/v2/solar/psm3-download.csv?"
query_api_key = config.query_api_key
geocode_api_key = config.geocode_api_key
email = config.email
so_file = os.getcwd() + '/analyze.so'
cMethods = ctypes.CDLL(so_file)

"""
geocodeAddress: 
    Forms a data request to positionstack API given region and country to retrieve latitude and longitude from
    returns longitude and latitude in array form
"""
def geocodeAddress(region, country):
    conn = http.client.HTTPConnection('api.positionstack.com')

    params = urllib.parse.urlencode({
        'access_key': geocode_api_key,
        'query': region,
        'country': country,
        'limit': 1,
    })

    conn.request('GET', '/v1/forward?{}'.format(params))

    res = conn.getresponse()
    data = res.read()
    jDict = json.loads(data.decode('utf-8'))
    jDict = jDict['data'][0]
    lat, lon = jDict['latitude'], jDict['longitude']
    return [lon, lat] # supposed to be ordered lon then lat

"""
convertPointsToString: 
    Given multiple longitude and latitude points, convert it into string used for the next API request
    returned string contains every point separated by commas and spaces(for every pair of points)
"""
def convertPointsToString(points):
    string = ""
    for i in range(len(points)):
        point = points[i]
        string += str(point[0]) +'%20'+ str(point[1])
        if i != len(points) - 1:
            string += "%2C"
    return string

"""
exportToDF: 
    Forms a data request based on pre-established values and downloads data
    into pandas DataFrame object and returns it
"""
def exportToDF(points):
    lat, lon, year = 32.9741,-106.2, 2020
    point_to_string = convertPointsToString(points)
    # Set the attributes to extract (e.g., dhi, ghi, etc.), separated by commas.
    attributes = 'ghi,dhi,dni,wind_speed,air_temperature,solar_zenith_angle'
    # Choose year of data
    year = '2020'
    # Set leap year to true or false. True will return leap day data if present, false will not.
    leap_year = 'false'
    # Set time interval in minutes, i.e., '30' is half hour intervals. Valid intervals are 30 & 60.
    interval = '30'
    # Specify Coordinated Universal Time (UTC), 'true' will use UTC, 'false' will use the local time zone of the data.
    # NOTE: In order to use the NSRDB data in SAM, you must specify UTC as 'false'. SAM requires the data to be in the
    # local time zone.
    utc = 'false'
    # Your full name, use '+' instead of spaces.
    your_name = 'Ethan+Nunez'
    # Your reason for using the NSRDB.
    reason_for_use = 'Academic'
    # Your affiliation
    your_affiliation = 'Rochester+Institute+of+Technology'
    email = 'ethanray2002@gmail.com'

    link = url+'&api_key={api}&wkt=MULTIPOINT({points})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&affiliation={affiliation}&reason={reason}&attributes={attr}&email={email}'.format(
        year=year, points=point_to_string, leap=leap_year, interval=interval, utc=utc, name=your_name, affiliation=your_affiliation, reason=reason_for_use, api=query_api_key, email=email, attr=attributes)
    # Return just the first 2 lines to get metadata:
    #print(link)
    info = pd.read_csv(link, nrows=1)
    # See metadata for specified properties, e.g., timezone and elevation
    timezone, elevation = info['Local Time Zone'], info['Elevation']
    #print(info)
    df = pd.read_csv(
        url+'api_key={api}&wkt=MULTIPOINT({points})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&affiliation={affiliation}&reason={reason}&attributes={attr}&email={email}'.format(
            year=year, points=point_to_string, leap=leap_year, interval=interval, utc=utc, name=your_name, affiliation=your_affiliation, reason=reason_for_use, api=query_api_key, email=email,
            attr=attributes), skiprows=2)
    #print(df.columns.values)
    #print(df['Temperature'].values)
    return df

"""
main: 
    Gets pandas df and conducts data mining methods on given data
"""
def main():
    point = geocodeAddress('Austin', 'US')
    #print("latitude and longitude of Austin in the US: " + str(point[0]) +"," + str(point[1]))

    df = exportToDF([point])
    '''values = df['Year'].values
    length = len(values)
    c_array_type = ctypes.c_double *length
    arr = c_array_type(*values)

    cMethods.centralTendency.argtypes = [ctypes.Array, ctypes.c_int]


    cMethods.centralTendency(arr, length)'''


main()