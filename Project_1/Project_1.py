#https://pypi.org/project/multitimer
#https://www.w3schools.com/python/python_mysql_getstarted.asp
#https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/ 
import mysql.connector
import Adafruit_DHT
import multitimer
from PyQt5 import QtWidgets, uic
import sys
import _thread
from datetime import datetime

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

USER="vatsal"
PASWWD="12345"
DATABASE="project1"
TABLE="sensor_data5"

def gui_thread():
  #global window
  app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
  window = Ui() # Create an instance of our class
  sys.exit(app.exec_()) # Start the application


#_thread.start_new_thread (gui_thread, ())

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

def read_data():
        #humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        humidity=1
        temperature=1
        now=datetime.now()
        mycursor.execute("INSERT INTO {} (humidity, temperature, time_stamp) VALUES ({}, {}, '{}')".format(TABLE, humidity, temperature, now))
        mydb.commit()
        ui.timer_upadte(temperature, humidity, now)
        print("TABLE")
        mycursor.execute("SELECT * FROM {}".format(TABLE))
        for x in mycursor:
            print(x)
 
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('project1_GUI.ui', self) # Load the .ui file
        self.button_refresh = self.findChild(QtWidgets.QPushButton, 'button_refresh') 
        self.button_refresh.clicked.connect(self.refresh_data)
        self.label_timestamp = self.findChild(QtWidgets.QLabel, 'label_timestamp') 
        self.label_temp = self.findChild(QtWidgets.QLabel, 'label_temp') 
        self.label_humidity = self.findChild(QtWidgets.QLabel, 'label_humidity') 
        self.label_time = self.findChild(QtWidgets.QLabel, 'label_time') 
        self.show() # Show the GUI
    
    def refresh_data(self):
        #humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        humidity=1
        temperature=1
        now=datetime.now()
        self.label_timestamp.setText(now.strftime("%m/%d/%Y, %H:%M:%S"))
      
    def timer_upadte(self, temp, hum, stamp):
        self.label_time.setText(stamp.strftime("%m/%d/%Y, %H:%M:%S"))
        self.label_temp.setText("{}".format(temp))
        self.label_humidity.setText("{}".format(hum))
         
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui()
    timer=multitimer.MultiTimer(3, read_data, args=None, kwargs=None, count=5, runonstart=True)
    timer.start()
    sys.exit(app.exec_())
