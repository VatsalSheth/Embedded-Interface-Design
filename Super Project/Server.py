"""
File Name: Server.py

Description: This code is used to interface rfid and Login Page. It creates MySQL database 
             and display these readings in a GUI

Date: 12/11/2019
References: https://www.w3schools.com/python/python_mysql_getstarted.asp
            https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/
"""

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow
import sys
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import mysql.connector
from datetime import datetime
import boto3         
import threading

__author__ = "Vatsal Sheth, Satya Mehta Siddhant Jajoo"
__copyright__ = "Copyright (C) 2019 by Vatsal Sheth, Satya Mehta and Siddhant Jajoo"

# Update Login credentials for db server before use
USER="vatsal"
PASWWD="12345"
DATABASE="Magic_Wand"
TABLE="Stats"

#Login Credentials
credential = {
    "Vatsal" :  "12345"        
}

#RFID Credentials
credential_rfid = [160630884818]

C_C = 0 
T_C = 0 
C_I = 0 
T_I = 0 
flag = 1

reader = SimpleMFRC522()

# Connect to db server 
mydb = mysql.connector.connect(
  host="localhost",
  user=USER,
  passwd=PASWWD, 
  buffered=True
)

mycursor = mydb.cursor()

# Create Database if not exists 
mycursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(DATABASE))
  
# Connect to db server on specific database  
mydb = mysql.connector.connect(
  host="localhost",
  user=USER,
  passwd=PASWWD,
  database=DATABASE,
  buffered=True
)

mycursor = mydb.cursor()

# Create Table if not exists
mycursor.execute("CREATE TABLE IF NOT EXISTS {} (id INT AUTO_INCREMENT PRIMARY KEY, Command VARCHAR(150), Status VARCHAR(5), time_stamp TIMESTAMP)".format(TABLE))

#S3 Client
#s3 = boto3.resource('s3')
s3 = boto3.client('s3')

class MainWindow(QtWidgets.QMainWindow):
    """
        MainWindow: This class inherits from QMainWindow and loads .ui file of Main Window. It consist of all the functions that would be
        required to display data on the GUI.
    """
    def __init__(self):
        """
            __init__: This constructor searches al child objects created in GUI and links it with local variable defined in class 
        """
        super(MainWindow, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('MainWindow.ui', self) # Load the .ui file
        self.Image = self.findChild(QtWidgets.QLabel, 'Image')
        self.button_refresh = self.findChild(QtWidgets.QPushButton, 'refresh_button') 
        self.button_refresh.clicked.connect(self.refresh_data)
        self.closea = self.findChild(QtWidgets.QPushButton, 'close') 
        self.closea.clicked.connect(self.close_app)
        self.correct_cmd = self.findChild(QtWidgets.QLabel, 'correct_cmd')
        self.incorrect_cmd = self.findChild(QtWidgets.QLabel, 'incorrect_cmd')
        self.total_cmd = self.findChild(QtWidgets.QLabel, 'total_cmd')
        self.per_cmd = self.findChild(QtWidgets.QLabel, 'per_cmd')
        self.correct_cmd2 = self.findChild(QtWidgets.QLabel, 'correct_cmd_2')
        self.incorrect_cmd2 = self.findChild(QtWidgets.QLabel, 'incorrect_cmd_2')
        self.total_cmd2 = self.findChild(QtWidgets.QLabel, 'total_cmd_2')
        self.per_cmd2 = self.findChild(QtWidgets.QLabel, 'per_cmd_2')
        self.image_label = self.findChild(QtWidgets.QLabel, 'image_label')
        
    def close_app(self):
        """
        close_app: App close button click event
        """
        global flag
        app.exit()
        flag = 0
        
    def refresh_data(self):
        """
        refresh_data: refresh button click event
        """
        s3.download_file('my-wand-project','image.jpg','./image.jpg')
        self.Image.setPixmap(QPixmap('image.jpg'))
        self.image_label.setText("{}".format(self.identify_label))
        
        
    def update_voice(self):
        """
        update_voice: Updates Voice command stats on GUI.
        """
        global C_C, C_I, T_C, T_I
        self.correct_cmd.setText("{}".format(C_C))
        self.incorrect_cmd.setText("{}".format(T_C-C_C))
        self.per_cmd.setText("{0:.2f} %".format((C_C/T_C)*100))
        self.total_cmd.setText("{}".format(T_C))
        
    def update_image(self,label):
        """
        update_image: Updates Image stats on GUI.
        """
        self.correct_cmd2.setText("{}".format(C_I))
        self.incorrect_cmd2.setText("{}".format(T_I-C_I))
        self.per_cmd2.setText("{0:.2f} %".format((C_I/T_I)*100))
        self.total_cmd2.setText("{}".format(T_I))
        self.identify_label = label

class Login(QtWidgets.QWidget):
    """
        Login: This class inherits from QWidgets and loads .ui file of Login Window. It consist of all the functions that would be
        required to display data on the GUI.
    """
    switch_window = QtCore.pyqtSignal()
        
    def __init__(self):
        """
            __init__: This constructor searches al child objects created in GUI and links it with local variable defined in class 
        """
        super(Login, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('Login.ui', self) # Load the .ui file
        self.button_login = self.findChild(QtWidgets.QPushButton, 'login_button') 
        self.button_login.clicked.connect(self.check_login)
        self.button_rfid = self.findChild(QtWidgets.QPushButton, 'rfid_button') 
        self.button_rfid.clicked.connect(self.check_rfid)
        self.login_mssg = self.findChild(QtWidgets.QLabel, 'login_mssg')
        self.username = self.findChild(QtWidgets.QLineEdit, 'username')
        self.password = self.findChild(QtWidgets.QLineEdit, 'password')

    def check_rfid(self):
        """
        check_rfid: RFID Auth
        """
        try:
                id, text = reader.read()
                if id in credential_rfid:
                    self.switch_window.emit()
                else:
                    self.login_mssg.setText("Invalid RFID")
        finally:
                GPIO.cleanup()
        
    def check_login(self):
        """
        check_login: Username & Password Auth
        """
        name = self.username.text()
        if name in credential:
            if self.password.text() == credential[name]:
                self.switch_window.emit()
            else:
               self.login_mssg.setText("Invalid Password") 
        else:
            self.login_mssg.setText("Invalid Username")

window = 0
class Controller:
    """
        Controller: This class controls transition between windows
    """
    def __init__(self):
        pass

    def show_login(self):
        """
        show_login: Displays Login Page
        """
        self.login = Login()
        self.login.switch_window.connect(self.show_main)
        self.login.show()
                
    def show_main(self):
        """
        show_main: Displays Main Window Page
        """
        global window,thread1
        window = MainWindow()
        self.login.close()
        window.show()
        thread1.start()
    
def sqs_thread():
    """
        sqs_thread: SQL management thread
    """
    global controller,mycursor, T_C, T_I, C_C, C_I,window, flag
    identity = 0
    
    while flag:
        mycursor.execute("SELECT * FROM Stats WHERE id > %s", (str(identity),))
        result = mycursor.fetchall()
        for x in range(len(result)):
            identity = result[x][0]
            if result[x][1] == 'voice':
                T_C+=1
                if result[x][2] == '1':
                    C_C+=1
                window.update_voice()
            else:
                T_I+=1
                if result[x][2] == '1':
                    C_I+=1
                window.update_image(result[x][1])

    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_login() 
    
    """Multithreading"""
    thread1 = threading.Thread(target = sqs_thread)
    sys.exit(app.exec_())
    print ("End !!!")
    thread1.join()
    
