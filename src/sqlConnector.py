#Connect information between database and local machine

#Get news category dictionary from sql database

import mysql.connector
import sys
import re

def newsDictCatcher():
    output = dict()
    conn = mysql.connector.connect(host='prod-mysql-nestia-food.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com',
                               user='readonly', password='nestiareadonly', database='news')
    cursor = conn.cursor()
    cursor.execute('select id, type from news')
    queryResult = cursor.fetchall()
    cursor.close()
    conn.close()
    for idTypePair in queryResult:
        try:
            if idTypePair[1] != -1:
                output.update({idTypePair[0]: idTypePair[1]})
        except:
            print('Error row: %s' % idTypePair)
    print('Get news dict successfully')
    return output

def getCurrentNewsProfile():
    currentNewsProfile = dict()
    conn = mysql.connector.connect(host='hsdb.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com',
                               user='HSDBADMIN', password='NestiaHSPWD', database='recommend_system')
    cursor = conn.cursor()
    cursor.execute('select device_id, newsProfile from user_data')
    queryResult = cursor.fetchall()
    cursor.close()
    conn.close()
    for idProfilePair in queryResult:
        deviceId = idProfilePair[0].decode('utf-8')
        try:
            Profile = idProfilePair[1].decode('utf-8')
        except:
            Profile = idProfilePair[1]
        currentNewsProfile.update({deviceId: Profile})
    return currentNewsProfile

def updateNewsProfile(outputDict):
    validIdPattern = re.compile('[0-9A-Za-z/-]{36,36}|[0-9a-z]{12,16}')
    outputFalse = []
    outputTrue = []

    outputLength = len(outputDict.keys())
    counter = 0
    conn = mysql.connector.connect(host='hsdb.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com',
                               user='HSDBADMIN', password='NestiaHSPWD', database='recommend_system')
    cursor = conn.cursor()

    for deviceId in outputDict.keys():
        if validIdPattern.match(deviceId):
            try:
                output = {'deviceId': deviceId, 'newsProfile': outputDict[deviceId]}
                if outputDict[deviceId].existInDB == False:
                    #outputFalse.append((deviceId, outputDict[deviceId].output))
                    cursor.execute('insert into user_data(device_id, newsProfile) values (%(deviceId)s, %(newsProfile)s)', output)
                else:
                    #outputTrue.append((outputDict[deviceId].output, deviceId))
                    cursor.execute('update user_data set newsProfile = %(newsProfile)s where device_id = %(deviceId)s', output)
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
        counter += 1
        sys.stdout.write('\r' + 'Executing: %s%%  ' % round((counter/outputLength) * 100, 1))
        sys.stdout.flush()  # important

    # cursor.executemany('insert into user_data(device_id, newsProfile) values (%s, %s)', outputFalse)
    # cursor.executemany('update user_data set newsProfile = %s where device_id = %s', outputTrue)
    conn.commit()
    cursor.close()
    conn.close()
