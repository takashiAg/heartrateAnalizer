import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from datetime import datetime as dt

filterCoefficient = 0.99


def readCsv(fileName):
    with open(fileName) as f:
        reader = csv.reader(f)
        header = next(reader)
        return [[dt.strptime(row[0], '%H:%M:%S'), float(row[1])] for row in reader]


def drawData(label, data):
    fig = plt.figure()

    # 図の中にサブプロットを追加する
    subPlots = []
    for d in range(len(data)):
        subPlot = fig.add_subplot(len(data), 1, d + 1)
        subPlot.xaxis.set_major_locator(mdates.HourLocator())
        subPlot.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
        subPlots.append(subPlot)

    for i, subPlot in enumerate(subPlots):
        fig1_a_1, = subPlot.plot(label, data[i])

    plt.show()


def main():
    # CSVからデータを読み込む
    data = readCsv("rawData20191014.csv")

    # 転地してtimeとheartrateに分割
    (time, heartRate) = np.array(data).T

    # digital filter
    filteredHeartRate = []
    print(0.0 * filterCoefficient)
    for HR in heartRate:
        filteredHeartRate.append(
            HR if len(filteredHeartRate) == 0
            else float(filteredHeartRate[-1]) * filterCoefficient
                 + float(HR) * (1.0 - filterCoefficient)
        )

    drawData(time, [heartRate, filteredHeartRate])


if __name__ == '__main__':
    main()
