import csv
import numpy as np
import matplotlib.pyplot as plt

username = "nakano"
filepath = "data/{username}/{filename}.csv"


def readCsv(fileName):
    with open(fileName) as f:
        reader = csv.reader(f)
        header = next(reader)
        return [[float(row[2]), float(row[3]), float(row[4])] for row in reader]


def main():
    notified_replied_timing = readCsv(filepath.format(username=username, filename="notified_replied_timing"))
    (time_respond, JIT_notify, JIT_respond) = np.array(notified_replied_timing).T
    print(notified_replied_timing)

    fig = plt.figure()

    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(time_respond, JIT_notify, c='red',label="JIT index at notified")
    ax.scatter(time_respond, JIT_respond, c='blue',label="JIT index at respond")

    # ax.set_title(' ')
    ax.set_xlabel('time to respond [min]')
    ax.set_ylabel('JIT index')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
