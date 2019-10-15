import csv
import numpy as np
import matplotlib.pyplot as plt

filterCoefficient = 0.99


def readCsv(fileName):
    with open(fileName) as f:
        reader = csv.reader(f)
        header = next(reader)
        return [[row[0], float(row[1])] for row in reader]


def drawData(label, data):
    fig = plt.figure()

    # 図の中にサブプロットを追加する
    subPlots = []
    for d in range(len(data)):
        subPlots.append(fig.add_subplot(len(data), 1, d + 1))

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

    print(len(time), len(heartRate), len(filteredHeartRate))

    print(time, heartRate, filteredHeartRate)
    x = np.linspace(-2 * np.pi, 2 * np.pi, 10000)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.tan(x)
    drawData(x, [y1, y2, y3])


if __name__ == '__main__':
    main()
