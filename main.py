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


def readTiming(goodTimingFileName, badTimingFileName):
    f = open(goodTimingFileName)
    reader = csv.reader(f)
    header = next(reader)
    goodTiming = [[dt.strptime(row[0], '%H:%M:%S'), dt.strptime(row[1], '%H:%M:%S')] for row in reader]
    f.close()

    f = open(badTimingFileName)
    reader = csv.reader(f)
    header = next(reader)
    badTiming = [[dt.strptime(row[0], '%H:%M:%S'), dt.strptime(row[1], '%H:%M:%S')] for row in reader]
    f.close()
    return (goodTiming, badTiming)


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


def drawHeartRate(label, heartRate, goodTiming):
    fig = plt.figure(figsize=(15.0, 10.0))

    # 図の中にサブプロットを追加する

    subPlotHeartRate = fig.add_subplot(2, 1, 1)
    subPlotHeartRate.xaxis.set_major_locator(mdates.HourLocator())
    subPlotHeartRate.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    subPlotHeartRate_ax, = subPlotHeartRate.plot(label, heartRate)

    subPlotHeartRate.set_xlabel("time [-]", fontsize=20)
    subPlotHeartRate.set_ylabel("Heart pulse [bpm]", fontsize=20)

    subPlotJustTiming = fig.add_subplot(2, 1, 2)
    subPlotJustTiming.xaxis.set_major_locator(mdates.HourLocator())
    subPlotJustTiming.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    subPlotJustTiming_ax, = subPlotJustTiming.plot(label, goodTiming)

    subPlotJustTiming.set_xlabel("time [-]", fontsize=20)
    subPlotJustTiming.set_ylabel("Just timing rate [-]", fontsize=20)

    # ラベルを縦向きに
    for ax in fig.axes:
        plt.sca(ax)
        plt.xticks(rotation=90)


def drawHistgram(datas):
    width = 0.3
    x_axis = np.arange(100)
    fig = plt.figure(figsize=(15.0, 10.0))

    subPlot = fig.add_subplot(1, 1, 1)
    # fig.xlim(40, 80)

    for i, data in enumerate(datas):
        subPlot.bar(x_axis + i * width, data, width=width, align='center')

    # ラベルを縦向きに
    for ax in fig.axes:
        ax.set_xlim(40, 80)
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


def calcJustTiming(data, filter1Coefficient, filter1Order, stdCount, filter2Coefficient, filter2Order):
    # digital filter
    for i in range(filter1Order):
        data = filter(data, filter1Coefficient)

    deviationdHeartRate = deviation(data)

    stddevHeartRate = stddev(data, stdCount)

    deviationstddevHeartRate = deviation(stddevHeartRate)

    data = np.sqrt(combine(deviationdHeartRate, deviationstddevHeartRate))

    for i in range(filter2Order):
        data = filter(data, filter2Coefficient)

    return data


def compareTiming(timing, Label):
    for label in Label:
        if (label[0] < timing <= label[1]):
            return True
    return False


def calcHistgram(time, justTiming, goodTiming, badTiming):
    goodTimngList = [0] * 100
    badTimngList = [0] * 100
    for i, timing in enumerate(justTiming):
        if compareTiming(time[i], goodTiming):
            goodTimngList[int(timing) if 0 <= timing < 100 else 99] += 1
        if compareTiming(time[i], badTiming):
            badTimngList[int(timing) if 0 <= timing < 100 else 99] += 1
    return [badTimngList, goodTimngList]


def main():
    # CSVからデータを読み込む
    data = readCsv("rawData20191014.csv")
    goodTiming, badTiming = readTiming("goodtiming.csv", "badtiming.csv")

    print(goodTiming, badTiming)

    # 転地してtimeとheartrateに分割
    (time, heartRate) = np.array(data).T

    justTimingv1 = calcJustTiming(heartRate, 0.99, 1, 60, 0.9, 1)
    justTimingv2 = calcJustTiming(heartRate, 0.99, 1, 12, 0.99, 1)
    justTimingv3 = calcJustTiming(heartRate, 0.99, 1, 12, 0.9, 4)
    justTimingv4 = calcJustTiming(heartRate, 0.7, 10, 12, 0.8, 10)

    goodhistgramv1 = calcHistgram(time, justTimingv1, goodTiming, badTiming)
    goodhistgramv2 = calcHistgram(time, justTimingv2, goodTiming, badTiming)
    goodhistgramv3 = calcHistgram(time, justTimingv3, goodTiming, badTiming)
    goodhistgramv4 = calcHistgram(time, justTimingv4, goodTiming, badTiming)

    # drawData(time, [
    #     heartRate,
    #     justTimingv1
    # ])
    drawHeartRate(time, heartRate, justTimingv1)
    drawHistgram(goodhistgramv1)

    drawData(time, [
        heartRate,
        justTimingv2
    ])

    drawHistgram(goodhistgramv2)
    drawData(time, [
        heartRate,
        justTimingv3
    ])

    drawHistgram(goodhistgramv3)
    drawData(time, [
        heartRate,
        justTimingv4
    ])
    drawHistgram(goodhistgramv4)
    plt.show()


if __name__ == '__main__':
    main()
