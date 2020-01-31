import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from datetime import datetime as dt
import math
# import sys

username = ""
filepath = "data/{username}/{filename}.csv"


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
    fig = plt.figure(figsize=(8.0, 5.0))

    # 図の中にサブプロットを追加する

    subPlotHeartRate = fig.add_subplot(2, 1, 1)
    subPlotHeartRate.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
    subPlotHeartRate.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    subPlotHeartRate_ax, = subPlotHeartRate.plot(label, heartRate)
    subPlotHeartRate.tick_params(labelbottom=False)

    # subPlotHeartRate.set_xlabel("time [-]", fontsize=12)
    subPlotHeartRate.set_ylabel("Heart pulse [bpm]", fontsize=14)

    subPlotJustTiming = fig.add_subplot(2, 1, 2)
    subPlotJustTiming.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
    subPlotJustTiming.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    subPlotJustTiming_ax, = subPlotJustTiming.plot(label, goodTiming)

    subPlotJustTiming.set_xlabel("time [min]", fontsize=14)
    subPlotJustTiming.set_ylabel("Just-in-Time index [-]", fontsize=14)

    # ラベルを縦向きに
    for ax in fig.axes:
        plt.sca(ax)
        plt.xticks(rotation=90)


def calcFulterCutoffFreq(Samplefreqency, filterCoefficient):
    r = 1 - filterCoefficient
    fc = Samplefreqency / (2 * math.pi) * math.acos((2 - (2 * r) - (r ** 2)) / (2 * (1 - r)))
    return fc


def drawHistgram(bad, good):
    width = 0.3
    x_axis = np.arange(100)
    fig = plt.figure(figsize=(15.0, 10.0))

    subPlot = fig.add_subplot(1, 1, 1)
    subPlot.set_xlabel("Just-in-Time index [-]", fontsize=30)
    subPlot.set_ylabel("Occurrence [-]", fontsize=30)
    subPlot.tick_params(labelsize=20)
    subPlot.legend(fontsize=18)
    # fig.xlim(40, 80)

    subPlot.bar(x_axis, bad, width=width, align='center', label='label of bad timing')
    subPlot.bar(x_axis + width, good, width=width, align='center', label='label of good timing')

    # ラベルを縦向きに
    for ax in fig.axes:
        ax.set_xlim(40, 80)
        plt.legend(loc='upper right', fontsize=30)
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


def writeCsv(fileName, data, header):
    with open(fileName, mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for d in data:
            writer.writerow(d)


def main():
    print(username)
    # sample rate
    Fs = 2

    # CSVからデータを読み込む
    data = readCsv(filepath.format(username=username, filename="rawData"))

    # 転地してtimeとheartrateに分割
    (time, heartRate) = np.array(data).T

    filter1Coefficient = 0.99
    filter1Order = 1
    stdCount = 300
    filter2Coefficient = 0.9
    filter2Order = 1

    Fc1 = calcFulterCutoffFreq(Fs, filter1Coefficient)
    Fc2 = calcFulterCutoffFreq(Fs, filter2Coefficient)

    print("filter 1 cutoff freqency is {filter1Cutoff}[Hz]\nfilter 2 cutoff freqency is {filter2Cutoff}[Hz]"
          .format(filter1Cutoff=Fc1, filter2Cutoff=Fc2))

    justTiming = calcJustTiming(heartRate, filter1Coefficient, filter1Order, stdCount, filter2Coefficient, filter2Order)

    writeCsv(
        filepath.format(username=username, filename="JITindex"),
        np.array([[t.strftime("%H:%M") for t in time], justTiming]).T,
        ["time", "\"JIT\" index"]
    )


if __name__ == '__main__':
    main()
