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

set_humidity = 30
set_temp = 25
set_alarm_t = 0
set_alarm_h = 0

USER="vatsal"
PASWWD="12345"
DATABASE="project1"
TABLE="sensor_data5"

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
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        #humidity=1
        #temperature=1
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
        self.label_alert = self.findChild(QtWidgets.QLabel, 'label_alert') 
        self.label_temp_os = self.findChild(QtWidgets.QLabel, 'label_temp_os') 
        self.label_humidity_os = self.findChild(QtWidgets.QLabel, 'label_humidity_os') 
        self.label_time_i = self.findChild(QtWidgets.QLabel, 'label_time_i') 
        self.label_temp = self.findChild(QtWidgets.QLabel, 'label_temp') 
        self.label_humidity = self.findChild(QtWidgets.QLabel, 'label_humidity') 
        self.label_time = self.findChild(QtWidgets.QLabel, 'label_time') 
        self.alert_temp = self.findChild(QtWidgets.QLabel, 'alert_temp')
        self.slide_temp = self.findChild(QtWidgets.QSlider, 'slide_temp')
        self.slide_temp.valueChanged.connect(self.update_temp_slider)
        self.update_temp_slider()
        self.alert_humidity = self.findChild(QtWidgets.QLabel, 'alert_humidity')
        self.slide_humidity = self.findChild(QtWidgets.QSlider, 'slide_humidity')
        self.slide_humidity.valueChanged.connect(self.update_humidity_slider)
        self.update_humidity_slider()
        self.show() # Show the GUI
        
    def update_temp_slider(self):
        global set_temp
        set_temp = self.slide_temp.value()
        self.alert_temp.setText("{}".format(set_temp))
        
    def update_humidity_slider(self):
        global set_humidity
        set_humidity = self.slide_humidity.value()
        self.alert_humidity.setText("{}".format(set_humidity))
    
    def refresh_data(self):
        #humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        humidity=1
        temperature=1
        now=datetime.now()
        self.label_temp_i.setText("{}".format(temperature))
        self.label_humidity_i.setText("{}".format(humidity))
        self.label_time_i.setText(now.strftime("%m/%d/%Y, %H:%M:%S"))
      
    def timer_upadte(self, temp, hum, stamp):
        self.label_time.setText(stamp.strftime("%m/%d/%Y, %H:%M:%S"))
        self.label_temp.setText("{}".format(temp))
        self.label_humidity.setText("{}".format(hum))
        self.check_alert(temp, hum)
        
    def check_alert(self, temp, hum):
        global set_temp, set_humidity, set_alarm_t, set_alarm_h
        if temp >= set_temp:
            set_alarm_t = 1
            self.label_temp_os.setText("Temperature Overshoot !!!")
        else:
            set_alarm_t = 0
            self.label_temp_os.setText("")
        if hum >= set_humidity:
            set_alarm_h = 1
            self.label_humidity_os.setText("Humidity Overshoot !!!")
        else:
            set_alarm_h = 0
            self.label_humidity_os.setText("")
        if set_alarm_t or set_alarm_h:
            self.label_alert.setText("ALARM !!!")
        else:
            self.label_alert.setText("")
            
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui()
    timer=multitimer.MultiTimer(5, read_data, args=None, kwargs=None, count=5, runonstart=True)
    timer.start()
    sys.exit(app.exec_())
