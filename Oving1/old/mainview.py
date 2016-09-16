from PySide.QtCore import *
from PySide.QtGui import *

class MainView(QMainWindow):
	def __init__(self):
		super(MainView, self).__init__()
		QCoreApplication.setApplicationName("Proglab Oving 2")
		self.init_ui()
	
	def init_ui(self):
		self.setWindowTitle("Rock Paper Scissors - Proglab Oving 2")
		self.setGeometry(500,500,500,400)
		self.show()
		