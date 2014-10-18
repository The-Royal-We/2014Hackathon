from __future__ import print_function
import json
import pymysql
import uuid
import bottle
from bottle import route, run, request, abort

def connect_to_mysql():
    conn = None
    try:
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='findme',autocommit=True)
    except:
        print(sys.exc_info()[0])
    return conn

def db_insert(latitude, longitude, altitude):
    conn = connect_to_mysql()
    id = None
    if conn is None:
        print ("smth went wrong with the connection") 
    else:
        id = uuid.uuid1()
        cur = conn.cursor()
        sqlQuery = "INSERT INTO location (id, longitude, latitude, altitude) VALUES (" + "'"+str(id) + "'"+"," + "'"+latitude+"'" + "," + "'"+longitude+"'"+ "," + "'"+altitude+"')"
        print(sqlQuery)
        cur.execute(sqlQuery)
        print(cur.description)
        print()
    cur.close()
    conn.close()
    return id

@route('/sharelocation', method='POST')
def put_document():
    data = request.body.readline()
    print (data)
    if not data:
        abort(400, 'No data received')
    entity = json.loads(data)
    print("INSERTING...")
    print(entity['latitude'])
    print(entity['longitude'])
    print(entity['altitude'])
    id = db_insert(entity['latitude'],entity['longitude'],entity['altitude'])
    print("----------------")
    print(id)
    return id

@route('/getLocation/:id', method='GET')
def getLocation(id):
    ident = str(id)
    conn = connect_to_mysql()
    cur = conn.cursor()
    sql = "SELECT latitude,longitude, altitude FROM location WHERE id =" + ident+";"
    try:
        cur.execute(sql)
        row = cur.fetchone()
        lat = row[0]
        lon = row[1]
        alt = row[2]
        jsonResp = "{\"lat\":\""+lat+"\",\"long\":\""+lon+"\",\"alt\":\""+alt+"\"}"
        cur.close()
        conn.close()
        return jsonResp
    except:
        print("could not recieve data with id " + ident)


run(host='localhost', port=8080)
