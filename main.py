import csv
import numpy as np


def readCsv(fileName):
    with open(fileName) as f:
        reader = csv.reader(f)
        header = next(reader)
        return [[row[0], int(row[1])] for row in reader]


def main():
    data = readCsv("rawData20191014.csv")
    data = np.array(data)
    print(data)


if __name__ == '__main__':
    main()
