"""
File: NREL_Request.py
Description: A program that performs Extract, Transform and Load operations
            on solar data from NREL and calls functions to analyze
            data using data mining methods
Language: Python 3.8
Author: Ethan Ray Nunez     ern1274@rit.edu
"""
import NREL_DataMining.src.Data_Preprocess as Preprocess ,NREL_DataMining.src.NREL_Methods as NREL
import NREL_DataMining.src.NREL_DataMethods as DM
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
    attribute_df = Preprocess.organize_dfs(df, [])

    #print(attribute_df['ALL'])
    #print(type(attribute_df['ALL']))
    #print(type(attribute_df['US']['California']))

    #gitprint(month_df)
    #print("Printing")
    #print(attribute_df['ALL'])
    #DM.prep_apriori(attribute_df['ALL'])
    #DM.prep_clustering(attribute_df['ALL'])
    print("Done")

main()