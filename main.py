import csv
import numpy as np

filterCoefficient = 0.99


def readCsv(fileName):
    with open(fileName) as f:
        reader = csv.reader(f)
        header = next(reader)
        return [[row[0], float(row[1])] for row in reader]


def main():
    # CSVからデータを読み込む
    data = readCsv("rawData20191014.csv")

    # 転地してtimeとheartrateに分割
    (time, heartRate) = np.array(data).T

    filteredHeartRate = []
    print(0.0 * filterCoefficient)
    for HR in heartRate:
        filteredHeartRate.append(
            HR if len(filteredHeartRate) == 0
            else float(filteredHeartRate[-1]) * filterCoefficient
                 + float(HR) * (1.0 - filterCoefficient)
        )

    print(len(time), len(heartRate))

    print(time, heartRate)


if __name__ == '__main__':
    main()
