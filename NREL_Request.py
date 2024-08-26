from NREL_DataMining import config
import os
import requests
import zipfile

url = "https://developer.nrel.gov/api/nsrdb/v2/solar/psm3-2-2-download.json"
cwd = os.getcwd()
zipPath =  cwd +'/SolarData.zip'
dirPath = cwd + '/Data'
api_key = config.api_key
email = config.email
def main():
    payload = "&api_key="+api_key + "&years=2021&leap_day=false&interval=60&utc=false&reason=Academic&wkt=MULTIPOINT(-106.22%2032.9741%2C-106.18%2032.9741%2C-106.1%2032.9741)"
    payload += "&email=" + email
    #payload = "&email=ethanray2002@gmail.com&limit=1&location_ids=681462&years=2020&equipment=one_axis&api_key=FsHVg0Q3SaooEN64zanpAnZwJ6EEZjBDLQvHZ4yD"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
    }
    response = requests.get(url, params=payload, headers=headers)
    #response = requests.get(url)
    print(response.text)
    downloadUrl = response.json()['outputs']['downloadUrl']
    print(downloadUrl)
    fileName = "SolarData.zip"
    response = requests.get(downloadUrl)
    with open(fileName, mode="wb") as file:
        file.write(response.content)

    with zipfile.ZipFile(zipPath, 'r') as zip:
        for member in zip.infolist():
            arr = member.filename.split("/")
            zip.extract(member, dirPath)
            os.rename(dirPath+"/"+member.filename, dirPath+"/"+arr[1])

    for filename in os.scandir(dirPath):
        f = os.path.join(dirPath, filename)
        if os.path.isfile(f):
            print(f)

main()