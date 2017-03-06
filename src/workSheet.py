import csv
import os
import re

newsDetailPattern = re.compile('/news/\d+$')
validIdPattern = re.compile('[0-9A-Za-z/-]{36,36}|[0-9a-z]{12,16}')

def dataProcessor(newsIdTypeDict, outputDict):
    with open(os.path.expanduser('/Users/Taran/Desktop/NestiaProjects/NewsUserProfileBuilder/src/sample.csv')
            , 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                print(row)
            except:
                print('file %s, line %d' % (0, reader.line_num))