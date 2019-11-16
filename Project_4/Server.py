from PyQt5 import QtWidgets, uic
import sys

class MainWindow(QtWidgets.QMainWindow):
	
	def __init__(self):
		"""
            __init__: This constructor searches al child objects created in GUI and links it with local variable defined in class 
        """
		super(Login, self).__init__() # Call the inherited classes __init__ method
		uic.loadUi('MainWindow.ui', self) # Load the .ui file

class Login(QtWidgets.QWidget):
    
    switch_window = QtCore.pyqtSignal()
        
	def __init__(self):
		"""
            __init__: This constructor searches al child objects created in GUI and links it with local variable defined in class 
        """
		super(Login, self).__init__() # Call the inherited classes __init__ method
		uic.loadUi('Login.ui', self) # Load the .ui file
		self.button_login = self.findChild(QtWidgets.QPushButton, 'button_refresh') 
        self.button_login.clicked.connect(self.check_login)
				
	def check_login(self):
		self.switch_window.emit()

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
