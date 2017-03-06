import csv

with open('./src/RetentionRate.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    print(reader.__next__())

f.close()