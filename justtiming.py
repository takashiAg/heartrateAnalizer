import re
import csv

fileName="data/nakano/replied_timing.csv"
text = '''
16:54

16:59
Nakano  17:08
Nakano  18:10
Nakano  18:50
Nakano  19:04
Yes
'''

reg = r'(\d{2}:\d{2})'

matched = re.findall(reg, text)

f = open(fileName, 'w')
writer = csv.writer(f)
writer.writerow(["time"])
for d in matched:
    writer.writerow([d])
f.close()

if __name__ == '__main__':
    pass
