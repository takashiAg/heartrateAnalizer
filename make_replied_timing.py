import re
import csv
import datetime

fileName = "justtiming_takatoshi_2.csv"

baseTime = datetime.time(hour=14, minute=39)
timeStep = datetime.timedelta(minutes=5)
count = 49

startTime = datetime.datetime.combine(datetime.date.today(), baseTime)

f = open(fileName, 'w')
writer = csv.writer(f)
writer.writerow(["time"])
for i in range(count):
    writer.writerow([(startTime + i * timeStep).strftime("%H:%M")])
f.close()

if __name__ == '__main__':
    pass
