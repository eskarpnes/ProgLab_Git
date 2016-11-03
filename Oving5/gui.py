from PyQt4.QtGui import *
from PyQt4.QtCore import *
from  PIL import Image
from PIL.ImageQt import ImageQt
import sys

def PILimgToQt(pilimage):
    imgQ = ImageQt(pilimage)    # convert PIL img to PIL.ImageQt obj
    return QImage(imageq)       # cast ImageQt obj to QImage (for qt to handle)
    
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        QCoreApplication.setOrganizationName("toffel enterprises")
        QCoreApplication.setApplicationName("Proglab oving 5")
        
        self.init_ui()
        
    def init_ui(self):
        mainWidget = QWidget()
        mainLayout = QVBoxLayout()
        buttons = QHBoxLayout()
        
        self.mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        self.setGeometry(1500,600,1000,600)
        self.setWindowTitle('ProgLab Oving 5')
        self.show()
        

def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
    
main()