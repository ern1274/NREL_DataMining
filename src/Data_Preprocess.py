import pandas as pd
"""
organize_by_month:
    Organizes pandas DataFrame data by month.
    The dataframe will formated into the result as follows: {'ALL': {}, 'US':{'California:{}}}
    in the format above, each 'empty' dictionary has months as its keys and each respective months data.

"""
def organize_by_month(df):
    organized_df = {'ALL': {}}
    # 'ALL' IS A MONTH DICT NOT REGION DICT consisting of all data organized regardless of region
    for country in df.keys():
        if country not in organized_df.keys():
            organized_df[country] = {}
        for region in df[country].keys():
            regional_df = df[country][region]

            if 'Month' not in regional_df.keys():
                print("Month does not exist as an attribute within the dataframe")
                return None

            lst = {}
            for index, row in regional_df.iterrows():
                month = row['Month']


                if month not in lst.keys():
                    lst[month] = []

                lst[month].append(row)
                organized_df[country][region] = lst

            organized_df['ALL'] = {**organized_df['ALL'], **lst}
    return organized_df


"""
organize_by_year: 
    Organizes pandas DataFrame data by year.
    The dataframe will formated into the result as follows: {'ALL': {}, 'US':{'California:{}}}
    in the format above, each 'empty' dictionary has years as its keys and each respective years data. 

"""
def organize_by_year(df):
    organized_df = {'ALL': {}}
    # 'ALL' IS A YEAR DICT NOT REGION DICT consisting of all data organized regardless of region
    for country in df.keys():
        if country not in organized_df.keys():
            organized_df[country] = {}
        for region in df[country].keys():
            regional_df = df[country][region]

            if 'Year' not in regional_df.keys():
                print("Year does not exist as an attribute within the dataframe")
                return None

            lst = {}
            for index, row in regional_df.iterrows():
                year = row['Year']

                if year not in lst.keys():
                    lst[year] = []

                lst[year].append(row)
                organized_df[country][region] = lst

            organized_df['ALL'] = {**organized_df['ALL'], **lst}
    return organized_df
"""
assign_temp_bucket: 
    Given a decimal number in form of string, 
    return a label with their respective temperature range
"""
def assign_temp_bucket(temp):
    #temp is string, have to convert to double then assign.
    temp = float(temp)
    if temp <= 20.0:
        return '<=20.0'
    elif temp <= 37.0:
        return '<=37.0'
    elif temp <= 70.0:
        return '<=70.0'
    elif temp <= 100.0:
        return '<=100.0'
    else:
        return '>100'


"""
organize_by_temperature: 
    Organizes pandas DataFrame data by temperature.
    The dataframe will formated into the result as follows: {'ALL': {}, 'US':{'California:{}}}
    in the format above, each 'empty' dictionary has temperature as its keys and each respective temperature data. 

"""
def organize_by_temperature(df):
    organized_df = {'ALL': {}}
    # 'ALL' IS A MONTH DICT NOT REGION DICT consisting of all data organized regardless of region
    for country in df.keys():
        if country not in organized_df.keys():
            organized_df[country] = {}
        for region in df[country].keys():
            regional_df = df[country][region]

            if 'Temperature' not in regional_df.keys():
                print("Month does not exist as an attribute within the dataframe")
                return None

            lst = {}
            for index, row in regional_df.iterrows():
                temperature = assign_temp_bucket(row['Temperature'])

                if temperature not in lst.keys():
                    lst[temperature] = []

                lst[temperature].append(row)
                organized_df[country][region] = lst

            organized_df['ALL'] = {**organized_df['ALL'], **lst}
    return organized_df
"""
assign_wind_bucket: 
    Given a decimal number in form of string, 
    return a label with their respective wind speed range
"""
def assign_wind_bucket(temp):
    #temp is string, have to convert to double then assign.
    temp = float(temp)
    if temp < 4.0:
        return 'Calm - Gentle Breeze'
    elif temp < 7.0:
        return 'Moderate - Strong Breeze'
    elif temp < 10.0:
        return 'Near - Severe Gale'
    elif temp <= 13:
        return 'Storm - Hurricane Forces'
    else:
        return 'Beyond Hurricane Forces'
"""
organize_by_wind_speed: 
    Organizes pandas DataFrame data by Wind Speed.
    The dataframe will formated into the result as follows: {'ALL': {}, 'US':{'California:{}}}
    in the format above, each 'empty' dictionary has Wind Speed as its keys and each respective Wind Speed data. 

"""
def organize_by_wind_speed(df):
    organized_df = {'ALL': {}}
    # 'ALL' IS A MONTH DICT NOT REGION DICT consisting of all data organized regardless of region
    for country in df.keys():
        if country not in organized_df.keys():
            organized_df[country] = {}
        for region in df[country].keys():
            regional_df = df[country][region]

            if 'Wind Speed' not in regional_df.keys():
                print("Month does not exist as an attribute within the dataframe")
                return None

            lst = {}
            for index, row in regional_df.iterrows():
                speed = assign_wind_bucket(row['Wind Speed'])

                if speed not in lst.keys():
                    lst[speed] = []

                lst[speed].append(row)
                organized_df[country][region] = lst

            organized_df['ALL'] = {**organized_df['ALL'], **lst}
    return organized_df
"""
bucket_data: 
    Given a piece of data in form of string and attribute to classify the data, 
    return a label with their respective attribute
"""
def bucket_data(attribute, data):
    if attribute == 'Month':
        return data
    elif attribute == 'Year':
        return data
    elif attribute == 'Temperature':
        return assign_temp_bucket(data)
    elif attribute == 'Wind Speed':
        return assign_wind_bucket(data)
    elif attribute == 'DNI':
        return round(data/100,1)*100
    elif attribute == 'GHI':
        return round(data/100,1)*100
    #print("Attribute doesn't exist yet")
    return data
"""
attribute_assignment_recurse: 
    Given a Pandas row of data, attributes to classify the row, 
    and index to indicate which attribute
    for each attribute, assign attribute label and recurse to assign the rest of attribute label
    if at the end of an attributes, return the row in an array. 
"""
def attribute_assignment_recurse(row, index, attributes):
    if index == len(attributes):
        return [row]
    atr = attributes[index]
    if atr not in row.keys():
        print("Attribute " + atr + " didnt exist")
        return attribute_assignment_recurse(row, index+1, attributes)
    data = bucket_data(atr, row[atr])
    return {data: attribute_assignment_recurse(row, index+1, attributes)}
"""
organize_by_attr:
    Given a dataframe, iterate each row and call recursive function to organize each row
    and culminate each row
    returns a organized dataframe organized by passed in attributes array
"""
def organize_by_attr(df, attributes):
    organized_df = {}
    for index, row in df.iterrows():
        lst = attribute_assignment_recurse(row, 0, attributes)
        organized_df = {**organized_df, **lst}
    return organized_df
"""
organize_dfs:
    given multiple regional DataFrames, and a list of attributes to organize the data by.
    organize each regional dataframe individually and culminate them into a larger dataframe
    'ALL' keyword refers to all organized data irrespective of region and country
"""
def organize_dfs(dfs, attributes):
    organized_df = {'ALL': {}}
    for country in dfs.keys():
        if country not in organized_df.keys():
            organized_df[country] = {}
        for region in dfs[country].keys():
            regional_df = dfs[country][region]
            if len(attributes) != 0:
                result = organize_by_attr(regional_df, attributes)
                organized_df[country][region] = result
                organized_df['ALL'] = {**organized_df['ALL'], **result}
            else:
                organized_df[country][region] = regional_df
                organized_df['ALL'] = {**organized_df['ALL'], **regional_df}
                organized_df['ALL'] = pd.DataFrame.from_dict(organized_df['ALL'])

    return organized_df