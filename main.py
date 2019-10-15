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
    fig = plt.figure(figsize=(15.0, 10.0))

    # 図の中にサブプロットを追加する
    subPlots = []
    for d in range(len(data)):
        subPlot = fig.add_subplot(len(data), 1, d + 1)
        subPlot.xaxis.set_major_locator(mdates.HourLocator())
        subPlot.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
        subPlots.append(subPlot)

    for i, subPlot in enumerate(subPlots):
        fig1_a_1, = subPlot.plot(label, data[i])

    # ラベルを縦向きに
    for ax in fig.axes:
        plt.sca(ax)
        plt.xticks(rotation=90)


def deviation(data):
    mean = np.mean(data)
    std = np.std(data)
    return [((d - mean) / std * 10) + 50 for d in data]


def filter(data, coefficient):
    filteredData = []
    for HR in data:
        filteredData.append(
            HR if len(filteredData) == 0
            else float(filteredData[-1]) * coefficient
                 + float(HR) * (1.0 - coefficient)
        )
    return filteredData


def stddev(data, n):
    stdData = []
    for i, HR in enumerate(data):
        stdData.append(np.std(data[0 if i < n else (i - n):i + 1]))
    return stdData


def combine(array1, array2):
    return [x * y for (x, y) in zip(array1, array2)]


def main():
    # CSVからデータを読み込む
    data = readCsv("rawData20191014.csv")

    # 転地してtimeとheartrateに分割
    (time, heartRate) = np.array(data).T

    # digital filter 1次
    filteredHeartRate = filter(heartRate, filterCoefficient)

    deviationHeartRate = deviation(heartRate)
    deviationFilteredHeartRate = deviation(filteredHeartRate)

    stddev1minHeartRate = stddev(heartRate, 12)
    stddev1minfilteredHeartRate = stddev(filteredHeartRate, 12)

    stddev5minHeartRate = stddev(heartRate, 60)
    stddev5minfilteredHeartRate = stddev(filteredHeartRate, 60)

    deviationstddev5minfilteredHeartRate = deviation(stddev5minfilteredHeartRate)
    justTiming = np.sqrt(combine(deviationHeartRate, deviationstddev5minfilteredHeartRate))
    filteredJustTimingv1 = filter(justTiming, 0.9)

    yData = [
        heartRate,
        filteredHeartRate,
        deviationFilteredHeartRate,
        stddev1minfilteredHeartRate,
        justTiming,
        filteredJustTimingv1
    ]

    drawData(time, yData)

    drawData(time, [
        heartRate,
        filteredJustTimingv1
    ])
    plt.show()


if __name__ == '__main__':
    main()
