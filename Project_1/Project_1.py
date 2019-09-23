#https://pypi.org/project/multitimer
#https://www.w3schools.com/python/python_mysql_getstarted.asp
#https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/ 
import mysql.connector
import Adafruit_DHT
import multitimer
from PyQt5 import QtWidgets, uic
import sys
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

set_humidity = 30
set_temp = 25
set_alarm_t = 0
set_alarm_h = 0
not_connect = 0
count = 0
conv_type = 0

USER="vatsal"
PASWWD="12345"
DATABASE="project1"
TABLE="sensor_data7"

mydb = mysql.connector.connect(
  host="localhost",
  user=USER,
  passwd=PASWWD,
  buffered=True
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
  database=DATABASE,
  buffered=True
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS {} (id INT AUTO_INCREMENT PRIMARY KEY, humidity FLOAT, temperature FLOAT, time_stamp TIMESTAMP)".format(TABLE))
mycursor.execute("SHOW TABLES")
for x in mycursor:
  print(x)

def read_data():
        global count
        count +=1 
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        now=datetime.now()
        if humidity is not None and temperature is not None:
            not_connect = 0
            mycursor.execute("INSERT INTO {} (humidity, temperature, time_stamp) VALUES ({}, {}, '{}')".format(TABLE, humidity, temperature, now))
            mydb.commit()
            ui.timer_upadte(temperature, humidity, now)
        else:
            not_connect = 1
            ui.timer_upadte("NC", "NC", now)
        if count >= 5:
            ui.close_app()
            
 
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('project1_GUI.ui', self) # Load the .ui file
        self.radioButton_c = self.findChild(QtWidgets.QRadioButton, 'radioButton_c') 
        self.radioButton_c.pressed.connect(self.radio_c)
        self.radioButton_f = self.findChild(QtWidgets.QRadioButton, 'radioButton_f') 
        self.radioButton_f.pressed.connect(self.radio_f)
        self.button_refresh = self.findChild(QtWidgets.QPushButton, 'button_refresh') 
        self.button_refresh.clicked.connect(self.refresh_data)
        self.button_temp = self.findChild(QtWidgets.QPushButton, 'button_temp') 
        self.button_temp.clicked.connect(self.draw_temp)
        self.button_humidity = self.findChild(QtWidgets.QPushButton, 'button_humidity') 
        self.button_humidity.clicked.connect(self.draw_humidity)
        self.label_disconnect = self.findChild(QtWidgets.QLabel, 'label_disconnect') 
        self.label_set_temp = self.findChild(QtWidgets.QLabel, 'label_set_temp') 
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
    
    def radio_c(self):
        global conv_type, set_temp
        conv_type = 0;
        self.label_set_temp.setText("Temperature (*C)")
        set_temp = ((set_temp-32)*5)/9
        self.slide_temp.setValue(set_temp)
    
    def radio_f(self):
        global conv_type, set_temp
        conv_type = 1;
        self.label_set_temp.setText("Temperature (*F)")
        set_temp = (set_temp*1.8) + 32
        self.slide_temp.setValue(set_temp)
        
    
    def draw_temp(self):
        mycursor.execute("SELECT temperature FROM {} ORDER BY id DESC LIMIT 10".format(TABLE))
        temp_data = list(mycursor)
        temp_arr = np.asarray(temp_data)
        mycursor.execute("SELECT time_stamp FROM {} ORDER BY id DESC LIMIT 10".format(TABLE))
        time_data = list(mycursor)
        time_arr = np.asarray(time_data)
        if conv_type == 1:
            plt.ylabel("Temperature *F")
            for x in range(10):
                temp_arr[x] = (temp_arr[x]*1.8)+32
        elif conv_type == 0:
            plt.ylabel("Temperature *C")
        print(temp_arr)
        print(time_arr)
        plt.plot(time_arr, temp_arr)
        plt.title("Temperature Graph")
        plt.xlabel("Time")
        
        plt.show()
        
    def draw_humidity(self):
        mycursor.execute("SELECT humidity FROM {} ORDER BY id DESC LIMIT 10".format(TABLE))
        humidity_data = list(mycursor)
        humidity_arr = np.asarray(humidity_data)
        mycursor.execute("SELECT time_stamp FROM {} ORDER BY id DESC LIMIT 10".format(TABLE))
        time_data = list(mycursor)
        time_arr = np.asarray(time_data)
        plt.plot(time_arr, humidity_arr)
        plt.title("Humidity Graph")
        plt.xlabel("Time")
        plt.ylabel("Humidity %")
        plt.show()
        
    def update_temp_slider(self):
        global set_temp
        set_temp = self.slide_temp.value()
        self.alert_temp.setText("{}".format(set_temp))
        
    def update_humidity_slider(self):
        global set_humidity
        set_humidity = self.slide_humidity.value()
        self.alert_humidity.setText("{}".format(set_humidity))
    
    def close_app(self):
        self.close()
        app.exit()
        
    def refresh_data(self):
        now=datetime.now()
        self.label_time_i.setText(now.strftime("%m/%d/%Y, %H:%M:%S"))
        if not_connect == 0:
            humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            if conv_type == 1:
                temperature = (temperature*1.8) + 32
                self.label_temp_i.setText("{0:.2f} *F".format(temperature))
            elif conv_type == 0:
                self.label_temp_i.setText("{0:.2f} *C".format(temperature))
            self.label_humidity_i.setText("{0:.2f}".format(humidity))
            self.check_alert(temperature, humidity)
        else:
            self.label_temp_i.setText("NC")
            self.label_humidity_i.setText("NC")
      
    def timer_upadte(self, temp, hum, stamp):
        self.label_time.setText(stamp.strftime("%m/%d/%Y, %H:%M:%S"))
        if temp == "NC":
            self.label_temp.setText("{}".format(temp))
            self.label_humidity.setText("{}".format(hum))
            self.label_disconnect.setText("Sensor Disconnected !!!")
        else:
            if conv_type == 1:
                temp = (temp*1.8) + 32
                self.label_temp.setText("{0:.2f} *F".format(temp))
            elif conv_type == 0:
                self.label_temp.setText("{0:.2f} *C".format(temp))    
            self.label_humidity.setText("{0:.2f}".format(hum))
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
