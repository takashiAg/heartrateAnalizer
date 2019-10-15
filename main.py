import csv


def readCsv(fileName):
    with open(fileName) as f:
        reader = csv.reader(f)
        return [row for row in reader]


def main():
    data = readCsv("rawData20191014.csv")
    print(data)


if __name__ == '__main__':
    main()
