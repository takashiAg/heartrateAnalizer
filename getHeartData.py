import urllib.request
import json
import datetime
import csv

id = 18717

year = 2020
month = 1
day = 28

# url = 'http://localhost:8080/api/heartrate/18717/2019/12/11'
url = 'http://131.113.137.5:3000/api/heartrate/{id}/{startTimestamp:.0f}/{stopTimestamp:.0f}' \
    .format(id=id, startTimestamp=datetime.datetime(year, month, day, 0, 0, 0, 0).timestamp() * 1000,
            stopTimestamp=datetime.datetime(year, month, day + 1, 0, 0, 0, 0).timestamp() * 1000)


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
        dt_jst_aware = datetime.datetime.fromtimestamp(d["timestamp"] / 1000,
                                                       datetime.timezone(datetime.timedelta(hours=9)))
        rawData.append({"time": "{0:%H:%M:%S}".format(dt_jst_aware), "heartRate": d["ComputedHeartRate"]})
    # print(rawData)
    f = open('data_{year}_{month}_{day}.csv'
             .format(year=year, month=month, day=day), 'w')
    writer = csv.writer(f)
    writer.writerow(["time", "heartRate"])
    for d in rawData:
        writer.writerow([d["time"], d["heartRate"]])
    f.close()


if __name__ == '__main__':
    main()
