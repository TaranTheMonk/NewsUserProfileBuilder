#Get news category dictionary from sql database

import mysql.connector

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
