from NREL_DataMining import config
import os
import requests
import zipfile
import ctypes

url = "https://developer.nrel.gov/api/nsrdb/v2/solar/psm3-2-2-download.json"
cwd = os.getcwd()
zipPath =  cwd +'/SolarData.zip'
dirPath = cwd + '/Data'
api_key = config.api_key
email = config.email
so_file = cwd + '/analyze.so'
cMethods = ctypes.CDLL(so_file)

def downloadData(downloadUrl):
    fileName = "SolarData.zip"
    response = requests.get(downloadUrl)
    with open(fileName, mode="wb") as file:
        file.write(response.content)

    with zipfile.ZipFile(zipPath, 'r') as zip:
        for member in zip.infolist():
            arr = member.filename.split("/")
            zip.extract(member, dirPath)
            os.rename(dirPath + "/" + member.filename, dirPath + "/" + arr[1])
    os.remove(zipPath)

def extractAndClean():
    #metadata = []
    #metadataValues = []
    headers = []
    values = []
    for filename in os.scandir(dirPath):
        f = os.path.join(dirPath, filename)
        if os.path.isfile(f):
            print(f)
            with open(f, mode="r") as file:
                lines = file.readlines()
                for h in range(len(lines)):
                    line = lines[h]
                    arr = line.split(',')
                    if h < 3: # For headers
                        #if len(metadata) == 0 and h == 0:
                        #    metadata = arr
                        #elif len(metadataValues) == 0 and h == 1:
                        #    metadataValues = arr
                        if len(headers) == 0 and h == 2:
                            headers = headers + arr
                    else:
                        for i in range(len(headers)):
                            if len(values) == i:
                                values.append([])
                            values[i].append(float(arr[i]))
    return headers, values

def main():
    payload = "&api_key="+api_key + "&years=2021&leap_day=false&interval=60&utc=false&reason=Academic&wkt=MULTIPOINT(-106.22%2032.9741%2C-106.18%2032.9741%2C-106.1%2032.9741)"
    payload += "&email=" + email
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
    }
    response = requests.get(url, params=payload, headers=headers)
    #response = requests.get(url)
    print(response.text)
    downloadUrl = response.json()['outputs']['downloadUrl']
    print(downloadUrl)
    downloadData(downloadUrl)

    headers, values = extractAndClean()
    length = len(values[0])
    c_array_type = ctypes.c_double *length
    arr = c_array_type(*values[0])

    cMethods.centralTendency.argtypes = [ctypes.Array, ctypes.c_int]


    cMethods.centralTendency(arr, length)

    # c type bindings here, make a stubbed function within c file that takes in the headers and values and prints them

main()