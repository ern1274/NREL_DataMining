"""
File: NREL_Request.py
Description: A program that performs Extract, Transform and Load operations
            on solar data from NREL and calls functions to analyze
            data using data mining methods
Language: Python 3.8
Author: Ethan Ray Nunez     ern1274@rit.edu
"""
from NREL_DataMining.src import Data_Preprocess ,NREL_Methods as NREL
import ctypes
import os
so_file = os.getcwd() + '/analyze.so'
cMethods = ctypes.CDLL(so_file)

"""
main: 
    Gets pandas df and conducts data mining methods on given data
"""
def main():
    #points, regions = locationRequests()
    points = []
    regions = []
    #point = geocodeAddress('Texas', 'US')
    #points.append(point)
    point = NREL.geocodeAddress('California', 'US')
    points.append(point)
    #regions.append('Texas,US')
    regions.append('California,US')
    df = NREL.exportToDF(points, regions)
    attribute_df = Data_Preprocess.organize_by_wind_speed(df)
    #gitprint(month_df)
    for attribute in attribute_df['ALL'].keys():
        print(attribute)
        for i in range(5):
            entry = attribute_df['ALL'][attribute][i]
            print(entry)
    '''for country in df.keys():
        for region in df[country].keys():
            regional_df = df[country][region]
            for index, row in regional_df.iterrows():
                print(row["Name"], row["Age"])
            for attribute in regional_df.keys():
                print("\nAttribute: " + attribute)
                values = regional_df[attribute].values
                length = len(values)
                c_array_type = ctypes.c_double * length
                arr = c_array_type(*values)

                cMethods.centralTendency.argtypes = [ctypes.Array, ctypes.c_int]

                cMethods.centralTendency(arr, length)
    values = df['Year'].values
    length = len(values)
    c_array_type = ctypes.c_double * length
    arr = c_array_type(*values)

    cMethods.centralTendency.argtypes = [ctypes.Array, ctypes.c_int]


    cMethods.centralTendency(arr, length)
    '''

main()