import sys
from path import *
from dijkstra import *
from csvReader import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(60, 50, 1800, 1500)
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle("London Underground")
        self.timeCompleterTimes = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00"," 12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00",
                                    "00:30", "01:30", "02:30", "03:30", "04:30", "05:30", "06:30", "07:30", "08:30", "09:30", "10:30", "11:30", "12:30", "13:30", "14:30", "15:30", "16:30", "17:30", "18:30", "19:30", "20:30", "21:30", "22:30", "23:30"]
        
       # self.setStyleSheet("background-color: grey;")
       # widget = QWidget()


        #widget.setLayout(layout)
       # self.setCentralWidget(widget)

        self.home()
        self.layout = QVBoxLayout(self)
        w = QWidget()
        p = QPalette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QColor(240, 240, 240))
        gradient.setColorAt(1.0, QColor(240, 160, 160))
        p.setBrush(QPalette.Window, QBrush(gradient))
        w.setPalette(p)
        w.setLayout(self.layout)


    def show_new_window(self):
        Dijkstra(self.start.text(), self.time.text())
        self.path = Path(self.start.text(), self.end.text())
        
        print("travel time: ", self.path.get_travel_time(), "mins\n")
        print("fastest route: ")
        for i in self.path.get_path():
            print(i)
            var = QLabel(i[0], self)
            self.layout.addWidget(self, var, 0, i)


        # for i in range(0, 500, 50):
        #     var = QLabel("HEllo WOrld", self)
        #     layout1.addWidget(var, i, i)




    def home(self):
        #autofill text input
        csv = csvReader("LondonUndergroundInfo.csv").get_csv()
        
        stations = []
        for i in csv:
            if (i[1] not in stations):
                stations.append(i[1])
            if (i[2] not in stations):
                stations.append(i[2])
                           
        completer = QCompleter(stations)
        completer.setCaseSensitivity(Qt.CaseInsensitive)

        self.timeCompleter = QCompleter(self.timeCompleterTimes)
        
        
        #start input
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Start:')
        
        self.start = QLineEdit(self)
        self.start.setPlaceholderText("Enter departure station")
        self.start.setFrame(False)
        self.start.setCompleter(completer)

        font = self.start.font()
        font.setItalic(True)
        self.start.setFont(font)
        #self.start.editingFinished.connect(self.test)
    
        self.start.move(90,15)
        self.start.resize(200,30)
        self.nameLabel.move(10,20)

        #end dest. input
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('End:')

        self.end = QLineEdit(self)
        self.end.setPlaceholderText("Enter destination station")
        self.end.setCompleter(completer)
        #self.end.editingFinished.connect(self.onEndClick) 

        self.end.move(90,50)
        self.end.resize(200,30)
        self.nameLabel.move(10,50)

        # Time input
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Departure\nTime:')

        self.time = QLineEdit(self)
        self.time.setPlaceholderText("Departure time")
        self.time.setCompleter(self.timeCompleter)

        self.time.move(90,85)
        self.time.resize(200,30)
        self.nameLabel.move(10,80)

        # label = QLabel(self)
        # pixmap = QPixmap('tube_map.gif')
        # label.setPixmap(pixmap)
        # label.setGeometry(80, 200, 1600, 1069)
        # pixmap1 = pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.FastTransformation)

        # label.setPixmap(pixmap)
        # label.setGeometry(80, 200, 1600, 1069)
       

        # layoutMain = QVBoxLayout()
        # layoutMain.addWidget(label)
        

        self.w = None
        self.button = QPushButton('Go', self)
        self.button.move(140,140)
        self.button.clicked.connect(lambda: self.show_new_window())
         
        # command = lambda:self.presidentPageClick()
 #   def check(home, self):
        #button.show()
      #  alert = QMessageBox()
      #  alert.setText('Take me to my route plz')
      #  alert.exec_()
            
##        if self.w is None:
##            self.w = NextWindow()    
##            self.w.show()
##            
##        else:
##            self.w.close()   

        #else:
            #self.w = None
        
# app =  QApplication([])
# app.setStyle('Fusion')
           
# w = MainWindow()
# w.show()
# app.exec_()
