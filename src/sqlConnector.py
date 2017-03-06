#Connect information between database and local machine

#Get news category dictionary from sql database

import mysql.connector
import sys

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
        Profile = idProfilePair[1].decode('utf-8')
        currentNewsProfile.update({deviceId: Profile})
    return currentNewsProfile

def updateNewsProfile(outputDict):
    outputLength = len(outputDict.keys())
    counter = 0
    conn = mysql.connector.connect(host='hsdb.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com',
                               user='HSDBADMIN', password='NestiaHSPWD', database='recommend_system')
    cursor = conn.cursor()
    for deviceId in outputDict.keys():
        output = {'deviceId': deviceId, 'newsProfile': outputDict[deviceId].output}
        if outputDict[deviceId].existInDB == False:
            cursor.execute('insert into user_data(device_id, newsProfile) values (%(deviceId)s, %(newsProfile)s)', output)
        else:
            cursor.execute('update user_data set newsProfile = %(newsProfile)s where device_id = %(deviceId)s', output)
        counter += 1
        sys.stdout.write('\r' + 'Executing: %s%%  ' % round((counter/outputLength) * 100, 1))
        sys.stdout.flush()  # important

    conn.commit()
    cursor.close()
    conn.close()
