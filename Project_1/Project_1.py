#https://pypi.org/project/multitimer
#https://www.w3schools.com/python/python_mysql_getstarted.asp
#https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/ 
import mysql.connector
import Adafruit_DHT
import multitimer
from PyQt5 import QtCore, QtGui, QtWidgets
from test import Ui_MainWindow

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

USER="satya"
PASWWD="satya@123"
DATABASE="project1"
TABLE="sensor_data5"

def read_data():
  humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
  #humidity=1
  #temperature=1
  mycursor.execute("INSERT INTO {} (humidity, temperature) VALUES ({}, {})".format(TABLE, humidity, temperature))
  mydb.commit()
  print("TABLE")
  mycursor.execute("SELECT * FROM {}".format(TABLE))
  for x in mycursor:
    print(x)
	
mydb = mysql.connector.connect(
  host="localhost",
  user=USER,
  passwd=PASWWD
)

mycursor = mydb.cursor()
 
mycursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(DATABASE))
mycursor.execute("SHOW DATABASES")
for x in mycursor:
  print(x)
  
mydb = mysql.connector.connect(
  host="localhost",
  user=USER,
  passwd=PASWWD,
  database=DATABASE
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS {} (humidity FLOAT, temperature FLOAT, time_stamp TIMESTAMP)".format(TABLE))
mycursor.execute("SHOW TABLES")
for x in mycursor:
  print(x)
  
tmp=Ui_MainWindow(object)
tmp.label_test.setText(_translate("MainWindow", "vatsal"))

timer=multitimer.MultiTimer(3, read_data, args=None, kwargs=None, count=5, runonstart=True)
timer.start()
