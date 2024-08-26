import requests

url = "https://developer.nrel.gov/api/nsrdb/v2/solar/psm3-2-2-download.json"
def main():
    payload = "&api_key=FsHVg0Q3SaooEN64zanpAnZwJ6EEZjBDLQvHZ4yD&years=2021&leap_day=false&interval=60&utc=false&email=ethanray2002@gmail.com&reason=Academic&wkt=MULTIPOINT(-106.22%2032.9741%2C-106.18%2032.9741%2C-106.1%2032.9741)"
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

main()