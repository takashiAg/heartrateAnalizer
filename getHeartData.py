import urllib.request
import json

id = 18717

year = 2019
month = 12
day = 11

# url = 'http://localhost:8080/api/heartrate/18717/2019/12/11'
url = 'http://localhost:8080/api/heartrate/{id}/{year}/{month}/{day}' \
    .format(id=id, year=year, month=month, day=day)


def get():
    print("request to {url} ...".format(url=url))
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        body = res.read()
        return json.loads(body)


def main():
    rawData = []
    data = get()
    for d in data:
        rawData.append({"time": d["timestamp"], "heartRate": d["ComputedHeartRate"]})
    print(rawData)


if __name__ == '__main__':
    main()
