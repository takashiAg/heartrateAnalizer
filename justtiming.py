import re
import csv

fileName="data/arisa/replied_timing.csv"
text = '''


リマインダー : 返信する

Arisa Ishihara  12:05
はい！


リマインダー : 返信する


リマインダー : 返信する

Arisa Ishihara  12:15
はい！


リマインダー : 返信する


リマインダー : 返信する


リマインダー : 返信する

Arisa Ishihara  12:23
:スマイル:


リマインダー : 返信する
12:30
リマインダー : 返信する

Arisa Ishihara  12:30
:スマイル:


リマインダー : 返信する
12:40
リマインダー : 返信する







リマインダー : 返信する


リマインダー : 返信する

Arisa Ishihara  12:45
:ぽっ:


リマインダー : 返信する


リマインダー : 返信する


リマインダー : 返信する

Arisa Ishihara  12:51
:スマイリー:


リマインダー : 返信する

Arisa Ishihara  12:57
:スマイル:


リマインダー : 返信する
13:05
リマインダー : 返信する

Arisa Ishihara  13:05
:にこっ:


リマインダー : 返信する


リマインダー : 返信する

Arisa Ishihara  13:15
:スマイル:


リマインダー : 返信する

Arisa Ishihara  13:21
:にこっ:


リマインダー : 返信する

Arisa Ishihara  13:25
:あはは:


リマインダー : 返信する
13:35
リマインダー : 返信する

Arisa Ishihara  13:36
:ニヤ:


リマインダー : 返信する
13:45
リマインダー : 返信する
13:50
リマインダー : 返信する

Arisa Ishihara  13:54
:にこっ:


リマインダー : 返信する

Arisa Ishihara  13:57
:スマイル:


リマインダー : 返信する

Arisa Ishihara  14:00
:スマイル:


リマインダー : 返信する
14:10
リマインダー : 返信する

Arisa Ishihara  14:12
:スマイリー:


リマインダー : 返信する
14:20
リマインダー : 返信する


リマインダー : 返信する

Arisa Ishihara  14:26
:にこっ:


リマインダー : 返信する
14:35
リマインダー : 返信する
新しいメッセージ
14:40
リマインダー : 返信する

Arisa Ishihara  14:41
:うふふ:


リマインダー : 返信する

Arisa Ishihara  14:45
:スマイリー:
14:45
終わります！！！


リマインダー : 返信する
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
