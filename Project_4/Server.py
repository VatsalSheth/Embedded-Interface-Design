from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
import sys
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import mysql.connector
from datetime import datetime

# Update Login credentials for db server before use
USER="vatsal"
PASWWD="12345"
DATABASE="Magic_Wand"
TABLE="Stats"

credential = {
    "Vatsal" :  "12345"        
}

credential_rfid = [160630884818]

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
mycursor.execute("CREATE TABLE IF NOT EXISTS {} (Command CHAR(50), Status BOOL, time_stamp TIMESTAMP)".format(TABLE))

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        """
            __init__: This constructor searches al child objects created in GUI and links it with local variable defined in class 
        """
        super(MainWindow, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('MainWindow.ui', self) # Load the .ui file

class Login(QtWidgets.QWidget):
    
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
        self.Image = self.findChild(QtWidgets.QLabel, 'Image')
        self.pixmap = QPixmap("./img.jpg")
        self.Image.setPixmap(pixmap)

    def check_rfid(self):
        try:
                id, text = reader.read()
                if id in credential_rfid:
                    self.switch_window.emit()
                else:
                    self.login_mssg.setText("Invalid RFID")
        finally:
                GPIO.cleanup()
        
    def check_login(self):
        name = self.username.text()
        if name in credential:
            if self.password.text() == credential[name]:
                self.switch_window.emit()
            else:
               self.login_mssg.setText("Invalid Password") 
        else:
            self.login_mssg.setText("Invalid Username")

class Controller:
    def __init__(self):
        pass

    def show_login(self):
        self.login = Login()
        self.login.switch_window.connect(self.show_main)
        self.login.show()
                
    def show_main(self):
        self.window = MainWindow()
        self.login.close()
        self.window.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_login()    
    sys.exit(app.exec_())
