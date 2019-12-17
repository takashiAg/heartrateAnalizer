import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from datetime import datetime as dt

def readCsv(fileName):
    with open(fileName) as f:
        reader = csv.reader(f)
        header = next(reader)
        return [[dt.strptime(row[0], '%H:%M:%S'), float(row[1])] for row in reader]

def drawHeartRate(label, heartRate):
    fig = plt.figure(figsize=(15.0, 10.0))

    # 図の中にサブプロットを追加する

    subPlotHeartRate = fig.add_subplot(1, 1, 1)
    subPlotHeartRate.xaxis.set_major_locator(mdates.HourLocator())
    subPlotHeartRate.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    subPlotHeartRate_ax, = subPlotHeartRate.plot(label, heartRate)

    subPlotHeartRate.set_xlabel("time [-]", fontsize=20)
    subPlotHeartRate.set_ylabel("Heart pulse [bpm]", fontsize=20)

    # ラベルを縦向きに
    for ax in fig.axes:
        plt.sca(ax)
        plt.xticks(rotation=90)

def main():

    # CSVからデータを読み込む
    data = readCsv("rawData20191014.csv")

    # 転地してtimeとheartrateに分割
    (time, heartRate) = np.array(data).T

    drawHeartRate(time, heartRate)

    plt.show()


if __name__ == '__main__':
    main()
