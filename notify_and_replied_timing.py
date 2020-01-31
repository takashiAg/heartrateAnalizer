import csv
from datetime import datetime as dt

username = "arisa"
filepath = "data/{username}/{filename}.csv"


def readCsv(fileName):
    with open(fileName) as f:
        reader = csv.reader(f)
        header = next(reader)
        return [[dt.strptime(row[0], '%H:%M')] for row in reader]


def writeCsv(fileName, data, header):
    with open(fileName, mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for d in data:
            writer.writerow(d)


def main():
    notified_timing = readCsv(filepath.format(username=username, filename="notified_timing"))
    replied_timing = readCsv(filepath.format(username=username, filename="replied_timing"))
    print(notified_timing, replied_timing)

    data = []
    pointer = 0
    for n in notified_timing:
        while (replied_timing[pointer][0] < n[0]):
            if len(replied_timing) - 1 <= pointer:
                print("break", len(replied_timing) - 1, pointer)
                break
            pointer += 1
        data.append([n[0].strftime("%H:%M"), replied_timing[pointer][0].strftime("%H:%M")])

    writeCsv(
        filepath.format(username=username, filename="notified_replied_timing"),
        data,
        ["notified timing", "replied timing"]
    )


if __name__ == '__main__':
    main()
