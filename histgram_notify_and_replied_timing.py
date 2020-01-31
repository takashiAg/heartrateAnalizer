import csv
import numpy as np
import matplotlib.pyplot as plt

username = ""
filepath = "data/{username}/{filename}.csv"


def readCsv(fileName):
    with open(fileName) as f:
        reader = csv.reader(f)
        header = next(reader)
        return [[float(row[2]), float(row[3]), float(row[4])] for row in reader]


def main():
    notified_replied_timing = readCsv(filepath.format(username=username, filename="notified_replied_timing"))
    # replied_less_than = [[row[0], row[1], row[2], row[2] - row[1]] for row in notified_replied_timing if row[0] <= 1]
    # (_, JIT_less_than, _, JIT_diff_less_than) = np.array(replied_less_than).T
    # replied_more_than = [[row[0], row[1], row[2], row[2] - row[1]] for row in notified_replied_timing if row[0] > 1]
    # (_, JIT_more_than, _, JIT_diff_more_than) = np.array(replied_more_than).T
    # print(notified_replied_timing)
    (_, JIT_notified, JIT_replied) = np.array(notified_replied_timing).T
    fig = plt.figure()

    ax = fig.add_subplot(1, 1, 1)

    ax.hist(
        [JIT_notified, JIT_replied],
        label=["Respond with in 1 [min]", "Respond after more than 1 [min]"],
    )
    # ax.hist(, label = , rwidth = 0.4)
    # ax.scatter(time_respond, JIT_notify, marker='x', label="JIT index at notified")

    # ax.set_title(' ')
    ax.set_ylabel('Time to respond [min]')
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
    # plt.legend()

    plt.show()


if __name__ == '__main__':
    main()
