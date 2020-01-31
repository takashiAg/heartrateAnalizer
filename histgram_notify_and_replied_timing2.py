import csv
import numpy as np
import matplotlib.pyplot as plt
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


def main():
    notified_timing = readCsv(filepath.format(username=username, filename="notified_timing"))
    replied_timing = readCsv(filepath.format(username=username, filename="replied_timing"))

    JITindex = readJITindex(username)

    JIT_notified = []
    jit_pointer = 0
    for n in notified_timing:
        while (JITindex[jit_pointer][0] < n[0]):
            if len(JITindex) - 1 <= jit_pointer:
                break
            jit_pointer += 1
        JIT_notified.append([n[0].strftime("%H:%M"), JITindex[jit_pointer][1]])

    JIT_replied = []
    jit_pointer = 0
    for n in replied_timing:
        while (JITindex[jit_pointer][0] < n[0]):
            if len(JITindex) - 1 <= jit_pointer:
                break
            jit_pointer += 1
        JIT_replied.append([n[0].strftime("%H:%M"), JITindex[jit_pointer][1]])

    fig = plt.figure()

    ax = fig.add_subplot(1, 1, 1)

    (_, JIT_notified) = np.array(JIT_notified).T
    (_, JIT_replied) = np.array(JIT_replied).T
    JIT_notified = [float(i) for i in JIT_notified]
    JIT_replied = [float(i) for i in JIT_replied]
    print(JIT_notified)
    print(JIT_replied)

    ax.hist(
        [JIT_notified, JIT_replied],
        label=["Notified timing", "Response timing"]
    )
    # plt.xticks(rotation=90)
    # ax.set_xticks([40,50,60,70,80])
    # ax.set_xticklabels([40,50,60,70,80])

    # ax.set_xlim(40,70)
    # ax.hist(, label = , rwidth = 0.4)
    # ax.scatter(time_respond, JIT_notify, marker='x', label="JIT index at notified")

    # ax.set_title(' ')
    ax.set_ylabel('count [-]')
    ax.set_xlabel('\"JIT\" index [-]')

    # fig = plt.figure()
    #
    # ax = fig.add_subplot(1, 1, 1)
    # ax.hist(
    #     [JIT_diff_less_than, JIT_diff_more_than],
    #     label=["Respond with in 1 [min]", "Respond after more than 1 [min]"],
    # )
    # ax.set_ylabel('Time to respond [min]')
    # ax.set_xlabel('\"JIT\" index [-]')

    plt.legend()

    plt.show()


if __name__ == '__main__':
    main()
