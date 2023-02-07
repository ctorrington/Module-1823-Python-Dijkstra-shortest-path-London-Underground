import sys
from csv import *
from path import *
from dijkstra import *
from csvReader import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import datetime

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.setWindowTitle("🚂 <- its a train")
        self.layout1 = QGridLayout(self)
        csv = csvReader("LondonUndergroundInfo.csv").get_csv()
        self.labellist = list()

        stations = []
        for i in csv:
            if (i[1] not in stations):
                stations.append(i[1])
            if (i[2] not in stations):
                stations.append(i[2])
        timeCompleterTimes = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00"," 12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00",
                                    "00:30", "01:30", "02:30", "03:30", "04:30", "05:30", "06:30", "07:30", "08:30", "09:30", "10:30", "11:30", "12:30", "13:30", "14:30", "15:30", "16:30", "17:30", "18:30", "19:30", "20:30", "21:30", "22:30", "23:30"]
                           
        completer = QCompleter(stations)
        completer.setCaseSensitivity(Qt.CaseInsensitive)

        timeCompleter = QCompleter(timeCompleterTimes)

        self.currentTime = datetime.datetime.now().time()
        self.currentTime = str(self.currentTime).split(":")
        
        self.start = QLineEdit("", self)
        self.start.setCompleter(completer)
        self.start.setPlaceholderText("start")
        self.end = QLineEdit("", self)
        self.end.setCompleter(completer)
        self.end.setPlaceholderText("end")
        self.time = QLineEdit("", self)
        self.time.setCompleter(timeCompleter)
        self.time.setPlaceholderText(self.currentTime[0] + ":" + self.currentTime[1])
        
        self.button = QPushButton('Go', self)
        self.button.clicked.connect(lambda: self.station_check(self.start.text(), self.end.text()))

        self.layout1.addWidget(self.start, 0, 0, 1, 2)
        self.layout1.addWidget(self.end, 1, 0, 1, 2)
        self.layout1.addWidget(self.time, 2, 0, 1, 2)
        self.layout1.addWidget(self.button, 3, 0, 1, 2)

        widget = QWidget()
        widget.setLayout(self.layout1)
        self.setCentralWidget(widget)
        self.show()
        
    def time_check(self, time):
        t = time[:2] + time[-2:]
        if (int(t) > 500):
            self.on_button_click()
        else:
            #TODO add a label displaying error on ui page
            print("Trains are not operational at entered time.")
        
    def station_check(self, station0, station1):
        csv = csvReader("LondonUndergroundInfo.csv").get_csv()
        s0 = False
        s1 = False
        for i in csv:
            if (i[1] == station0 or i[2] == station0):
                s0 = True
            elif (i[1] == station1 or i[2] == station1):
                s1 = True
            else:
                continue
        
        if (s0 and s1):
            if (self.time.text() == ""):
                self.time_check(self.currentTime[0] + ":" + self.currentTime[1])    
            else:
                self.time_check(self.time.text())
        elif (not s0 and not s1):
            QMessageBox.critical(self, "ERROR", "Neither stations in station list!")
            self.start.clear()
            self.end.clear()
            self.start.setFocus()
        elif (not s0):
            QMessageBox.critical(self, "ERROR", "Start station not in station list!")
            self.start.clear()
            self.start.setFocus()
        elif (not s1):
            QMessageBox.critical(self, "ERROR", "Destination station not in station list!")
            self.end.clear()
            self.end.setFocus()
            
        
    def on_button_click(self):
        if not self.labellist: 
            Dijkstra(self.start.text(), self.currentTime[0] + ":" + self.currentTime[1])
            self.path = Path(self.start.text(), self.end.text())
            print("travel time: ", self.path.get_travel_time(), "mins\n")
            print("fastest route: ")
            for index, i in enumerate(self.path.get_path()):
                print(i)
                if (index == 0):
                    station = QLabel(i, self)
                    self.labellist.append(station)
                    self.layout1.addWidget(station, int(index + 4), 1)
                else:
                    station = QLabel("♿ " + i[0], self)
                    self.labellist.append(station)
                    Line = QLabel(i[1], self)
                    self.labellist.append(Line)
                    totalTravel = QLabel(str(i[3]), self)
                    self.labellist.append(totalTravel)
                    self.layout1.addWidget(station, int(index + 4), 1)
                    self.layout1.addWidget(Line, int(index + 4), 0)
                    self.layout1.addWidget(totalTravel, int(index + 4), 2)
                    totalTravel.setAlignment(Qt.AlignRight)
        else: 
            for i in self.labellist:
                self.labellist.remove(i)
                i.clear()
            self.on_button_click()

app =  QApplication([])
app.setStyle('Fusion')
        
window = Ui()
window.show()
app.exec_()
