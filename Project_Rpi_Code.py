# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 21:34:51 2020

@author: Ashner_Novilla
"""
import serial
from time import sleep
import mysql.connector
import http.client, urllib


key = 'EZ4JTTHPOOJUUE3D'

arduinoData = serial.Serial('/dev/ttyUSB1',9600)

def database():
    mydb = mysql.connector.connect(
      host="dbinstance360.cedkdqudpuco.us-east-2.rds.amazonaws.com",
      user="admin",
      password="ashnern0villa",
      database="testDB"
    )
    mycursor = mydb.cursor()

    sql = "INSERT INTO iotdb (humidity, temperature, soil_moisture) VALUES (%s, %s, %s)"
    val = (humidity, temperature, soil_moisture)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    print(mydb)  
    
def thingspeak():
        params = urllib.parse.urlencode({'field1': temperature,'field2': humidity, 'field3': soil_moisture,'key':key })
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = http.client.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print ('temepera : ',temperature)
            print ('humidity : ',humidity)
            print ('soil_moi : ',soil_moisture )
            print (response.status, response.reason)
            #data = response.read()
            conn.close()
        except:
            print ("connection failed")

def writedata():
    sleep(5)
    arduinoData.write('s'.encode())
    sleep(1)

if __name__ == '__main__':
    while(True):
        writedata()
        
        rdata = arduinoData.readline().decode()
        sleep(1)
        pieces = rdata.split("\t")
        humidity = pieces[0]
        temperature = pieces[1]
        soil_moisture = pieces[2]
        
        print(humidity)
        print(temperature)
        print(soil_moisture)
        
        database()
        thingspeak()
        
        sleep(30)