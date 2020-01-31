import csv
from datetime import datetime as dt

username = "arisa"
filepath = "data/{username}/{filename}.csv"


def readCsv(fileName):
    with open(fileName) as f:
        reader = csv.reader(f)
        header = next(reader)
        return [[dt.strptime(row[0], '%H:%M')] for row in reader]


def readJITindex(username):
    fileName = "data/{username}/JITindex.csv".format(username=username)
    with open(fileName) as f:
        reader = csv.reader(f)
        header = next(reader)
        return [[dt.strptime(row[0], '%H:%M'), float(row[1])] for row in reader]


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

    JITindex = readJITindex(username)
    print("JIT index")
    print(JITindex)

    data = []
    pointer = 0
    jit_pointer = 0
    jit_pointer2 = 0
    for n in notified_timing:
        while (replied_timing[pointer][0] < n[0]):
            if len(replied_timing) - 1 <= pointer:
                break
            pointer += 1

        while (JITindex[jit_pointer][0] < n[0]):
            if len(JITindex) - 1 <= jit_pointer:
                break
            jit_pointer += 1

        while (JITindex[jit_pointer2][0] < replied_timing[pointer][0]):
            if len(JITindex) - 1 <= jit_pointer2:
                break
            jit_pointer2 += 1
        diff = (replied_timing[pointer][0] - n[0]).total_seconds() / 60
        diff = int(diff) if diff >= 0 else 0
        data.append([n[0].strftime("%H:%M"), replied_timing[pointer][0].strftime("%H:%M"), diff,
                     int(JITindex[jit_pointer][1]), int(JITindex[jit_pointer2][1])])

    writeCsv(
        filepath.format(username=username, filename="notified_replied_timing"),
        data,
        ["notified timing", "replied timing", "time to respond [min]", "JIt index at notified", "JIT index at replied"]
    )


if __name__ == '__main__':
    main()
