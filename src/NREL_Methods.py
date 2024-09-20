
from NREL_DataMining.src import config


import pandas as pd
import http.client, urllib.parse
import json

url = "https://developer.nrel.gov/api/nsrdb/v2/solar/psm3-2-2-download.csv?"
#url = "https://developer.nrel.gov/api/nsrdb_api/solar/spectral_ondemand_download.json?"
#above url requires data to be downloaded from zip and requires equipment=one_axis as parameter
query_api_key = config.query_api_key
geocode_api_key = config.geocode_api_key
email = config.email

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
    res.close()
    conn.close()
    jDict = json.loads(data.decode('utf-8'))
    if 'error' not in jDict.keys():
        jDict = jDict['data'][0]
        lat, lon = jDict['latitude'], jDict['longitude']
        return [lon, lat] # supposed to be ordered lon then lat
    print("Region and Country does not exist")
    return None

def locationRequests():
    points = []
    regions = []
    print("Only country available is the US due to difficulties requesting international api data")
    while True:
        addLoc = input("Add Region and Country? 'Y/y': Yes, 'N/n' : No ==> ")
        if str.lower(addLoc) == 'y':
            region = input("What region are you adding? ==> ")
            country = input("What country is this region located in? ==> ")
            point = geocodeAddress(region,country)
            if point is not None and country == 'US':
                regions.append(region+','+country)
                points.append(point)
            else:
                print("Region " + region + " within Country " + country + " is not available and/or couldn't be geocoded")
        elif str.lower(addLoc) == 'n':
            break
        else:
            print("Didn't recognize command, please try again")
    return points, regions


"""
convertPointsToString: 
    Given multiple longitude and latitude points, convert it into string used for the next API request
    returned string contains every point separated by commas and spaces(for every pair of points)
"""
def convertPointsToString(points):
    strings = []
    for point in points:
        strings.append(str(point[0]) +'%20'+ str(point[1]))
    return strings

"""
exportToDF: 
    Forms a data request based on pre-established values and downloads data
    into pandas DataFrame object and returns it
"""
def exportToDF(points, regions):
    lat, lon, year = 32.9741,-106.2, 2020
    points = convertPointsToString(points)
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
    country_dfs = {}
    for i in range(len(points)):
        point = points[i]
        region, country = regions[i].split(',')
        #print(region)
        #print(country)
        if country not in country_dfs.keys():
            country_dfs[country] = {}
        link = url+'&api_key={api}&wkt=POINT({point})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&affiliation={affiliation}&reason={reason}&attributes={attr}&email={email}'.format(
            year=year, point=point, leap=leap_year, interval=interval, utc=utc, name=your_name, affiliation=your_affiliation, reason=reason_for_use, api=query_api_key, email=email, attr=attributes)

        # Return just the first 2 lines to get metadata:
        #print(link)
        info = pd.read_csv(link, nrows=1)
        # See metadata for specified properties, e.g., timezone and elevation
        #timezone, elevation = info['Local Time Zone'], info['Elevation']
        #print(info)
        df = pd.read_csv(
            url+'api_key={api}&wkt=POINT({point})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&affiliation={affiliation}&reason={reason}&attributes={attr}&email={email}'.format(
                year=year, point=point, leap=leap_year, interval=interval, utc=utc, name=your_name, affiliation=your_affiliation, reason=reason_for_use, api=query_api_key, email=email,
                attr=attributes), skiprows=2)
        country_dfs[country][region] = df
        print("Region and Country "+regions[i] + " df downloaded")
    return country_dfs
