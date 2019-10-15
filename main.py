import csv
import numpy as np


def readCsv(fileName):
    with open(fileName) as f:
        reader = csv.reader(f)
        header = next(reader)
        return [[row[0], int(row[1])] for row in reader]


def main():
    # CSVからデータを読み込む
    data = readCsv("rawData20191014.csv")

    # 転地してtimeとheartrateに分割
    (time, heartRate) = np.array(data).T

    print(time, heartRate)


if __name__ == '__main__':
    main()
