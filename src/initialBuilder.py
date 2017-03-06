#Build initial user profile
from datetime import datetime
import time
import sys
import sqlConnector
import os
import csv
import re
import numpy as np
import json
import pandas as pd

class UserProfile():
    def __init__(self, deviceId, currentProfile):
        self.deviceId = deviceId
        self.vector, self.newsActiveDay, self.appActiveDay = self.initializeProfile(currentProfile)
        self.existInDB = False
        self.newsTypeHistory = list()
        self.output = None

    def turnOnExistingPara(self):
        self.existInDB = True

    def initializeProfile(self, currentProfile):
        if currentProfile == None:
            return np.array([0] * 28), 0, 0
        else:
            try:
                profile = json.loads(currentProfile)
                return profile['vector'], profile['newsActiveDay'], profile['appActiveDay']
            except:
                print('Wrong input:')
                print('%s : %s' % (self.deviceId, currentProfile))
                return np.array([0] * 28), 0, 0

    def buildVector(self):
        tempVector = np.array([0] * 28)
        for newsType in self.newsTypeHistory:
            tempVector[newsType - 1] += 1
        self.vector += tempVector

    def buildOutput(self):
        output = {'vector': self.vector.tolist(), 'newsActiveDay': self.newsActiveDay, 'appActiveDay': self.appActiveDay}
        self.output = json.dumps(output)

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
    newsId = int(row[1].split('/')[-1])
    newsType = newsIdTypeDict[newsId]
    if row[5] not in outputDict.keys():
        ##[[vector], news active day, app active day]
        outputDict.update({row[5]: UserProfile(row[5], None)})
    if newsType != -1:
        outputDict[row[5]].newsTypeHistory.append(newsType)

def dataProcessor(startDate, newsIdTypeDict, outputDict):
    with open(os.path.expanduser('~/nestia_logs_with_parameters/data-' + startDate + '.csv')
            , 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                if validIdPattern.search(row[5]):
                    appActiveSet.add(row[5])
                    if newsDetailPattern.search(row[1]):
                        newsActiveSet.add(row[5])
                        newsInformationCatcher(row, newsIdTypeDict, outputDict)
                if row[5] not in outputDict.keys():
                    outputDict.update({row[5]: UserProfile(row[5], None)})
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            print('file %s, line %d' % (startDate, reader.line_num))

def main():
    #Global variables
    global newsDetailPattern, validIdPattern, newsActiveSet, appActiveSet
    newsDetailPattern = re.compile('/news/\d+$')
    validIdPattern = re.compile('[0-9A-Za-z/-]{36,36}|[0-9a-z]{12,16}')

    #Set parameters, configs and output
    try:
        startDate, stopDate = getSysArgs()
    except:
        raise ParameterError()
    newsIdTypeDict = sqlConnector.newsDictCatcher()
    currentNewsProfile = sqlConnector.getCurrentNewsProfile()
    outputDict = dict()
    for deviceId in currentNewsProfile.keys():
        outputDict.update({deviceId: UserProfile(deviceId, currentNewsProfile[deviceId])})
        outputDict[deviceId].turnOnExistingPara()
    print('Essential parameters, configs and output built successfully')

    #Processing
    while startDate != stopDate:
        print('Processing: %s, stop at: %s' % (startDate, stopDate))
        newsActiveSet = set()
        appActiveSet = set()
        dataProcessor(startDate, newsIdTypeDict, outputDict)
        startDate = oneMoreDay(startDate)
        for deviceId in appActiveSet:
            outputDict[deviceId].appActiveDay += 1
        for deviceId in newsActiveSet:
            outputDict[deviceId].newsActiveDay += 1
    print('Process successfully')

    #Buidling output


    for deviceId in outputDict.keys():
        outputDict[deviceId].buildVector()
        outputDict[deviceId].buildOutput()
    print('Output build successfully')

    sqlConnector.updateNewsProfile(outputDict)
    print('Update successfully')


if __name__ == '__main__':
    main()