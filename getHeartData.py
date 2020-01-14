import urllib.request
import json
import datetime
import csv

id = 18717

year = 2019
month = 12
day = 10

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
        dt_jst_aware = datetime.datetime.fromtimestamp(d["timestamp"] / 1000,
                                                       datetime.timezone(datetime.timedelta(hours=9)))
        rawData.append({"time": "{0:%H:%M:%S}".format(dt_jst_aware), "heartRate": d["ComputedHeartRate"]})
    print(rawData)
    f = open('data_{year}_{month}_{day}.csv'
             .format(year=year, month=month, day=day), 'w')
    writer = csv.writer(f)
    writer.writerow(["time", "heartRate"])
    for d in rawData:
        writer.writerow([d["time"], d["heartRate"]])
    f.close()


if __name__ == '__main__':
    main()
