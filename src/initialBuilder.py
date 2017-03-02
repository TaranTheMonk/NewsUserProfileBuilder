#Build initial user profile
from datetime import datetime
import time
import sys
from src import sqlConnector
import os
import csv
import re

class UserProfileVector():
    def __init__(self, deviceId):
        self.deviceId = deviceId
        self.vector = None
        self.appActiveDay = 0
        self.newsActiveDay = 0

class ParameterError(Exception):
    def __str__(self):
        return '\nWrong input, command should be:\npython initialBuilder.py startDate stopDate'

def oneMoreDay(previousDay):
    currentValue = time.mktime(time.strptime(previousDay, "%Y-%m-%d"))
    currentValue += 24*60*60
    future = datetime.strftime(datetime.fromtimestamp(currentValue), "%Y-%m-%d")
    return future

##Command should be as follow
##python initialBuilder startDate stopDate
def getSysArgs():
    print('Number of arguments:', len(sys.argv) - 1, 'arguments.')
    print('Argument List:', sys.argv[1:])
    startDate = sys.argv[1]
    stopDate = sys.argv[2]
    print('Start Date:', startDate)
    print('Stop Date:', stopDate)
    return startDate, stopDate

def newsInformationCatcher(row, newsIdTypeDict, outputDict):
    if newsDetailPattern.search(row[1]):
        newsId = int(row[1].split('/')[-1])
        newsType = newsIdTypeDict[newsId]
    if row[5]
    return

def dataProcessor(startDate, newsIdTypeDict, outputDict):
    with open(os.path.expanduser('~/nestia_logs_with_parameters/data-' + startDate + '.csv')
            , 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                if validIdPattern.search(row[5]):
                    newsInformationCatcher(row, newsIdTypeDict, outputDict)
        except:
            print('file %s, line %d' % (startDate, reader.line_num))

def main():
    #Set parameters, configs and output
    global newsDetailPattern, validIdPattern
    newsDetailPattern = re.compile('/news/\d+$')
    validIdPattern = re.compile('[0-9A-Za-z/-]{36,36}|[0-9a-z]{12,16}')
    try:
        startDate, stopDate = getSysArgs()
    except:
        raise ParameterError()
    newsIdTypeDict = sqlConnector.newsDictCatcher()
    outputDict = dict()


    #Processing
    while startDate != stopDate:
        print('Processing: %s, stop at: %s' % (startDate, stopDate))
        dataProcessor(startDate, newsIdTypeDict, outputDict)
    return

if __name__ == '__main__':
    main()