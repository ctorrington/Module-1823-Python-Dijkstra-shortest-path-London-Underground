import datetime
import math
from csv import *

import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from csvReader import *
from dijkstra import *
from path import *

#create main window
class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.setWindowTitle("🚂 London Underground")
        self.layout1 = QGridLayout(self)
        self.csv = csvReader("LondonUndergroundInfo.csv").get_csv()
        self.labellist = list()
        self.largestPath = 0

        stations = []
        for i in self.csv:
            if (i[1] not in stations):
                stations.append(i[1])
            if (i[2] not in stations):
                stations.append(i[2])

        timeCompleterTimes = ["00:00", "00:30", "01:00", "01:30", "02:00", "02:30", "03:00", "03:30", "04:00", "04:30", "05:00", "05:30", "06:00", "06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", 
                              "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00", "23:30"]

        completer = QCompleter(stations)
        completer.setCaseSensitivity(Qt.CaseInsensitive)

        timeCompleter = QCompleter(timeCompleterTimes)

        self.currentTime = datetime.datetime.now().time()
        self.currentTime = str(self.currentTime).split(":")

        self.start = QLineEdit("", self)
        self.start.setCompleter(completer)
        self.start.setPlaceholderText("start")
        self.start.setFont(QFont("Comic Sans", 8))
        self.end = QLineEdit("", self)
        self.end.setFont(QFont("Comic Sans", 8))
        self.end.setCompleter(completer)
        self.end.setPlaceholderText("end")
        self.time = QLineEdit("", self)
        self.time.setFont(QFont("Comic Sans", 8))
        self.time.setCompleter(timeCompleter)
        self.time.setPlaceholderText(self.currentTime[0] + ":" + self.currentTime[1])

        self.button = QPushButton('Go', self)
        self.button.setFont(QFont("Comic Sans", 8))
        self.button.clicked.connect(lambda: self.station_check(self.start.text(), self.end.text()))

        self.layout1.addWidget(self.start, 2, 1, 1, 1)
        self.layout1.addWidget(self.end, 2, 2, 1, 1)
        self.layout1.addWidget(self.time, 2, 3, 1, 1)
        self.layout1.addWidget(self.button, 3, 2, 1, 1)

        self.widget = QWidget()
        self.widget.setLayout(self.layout1)
        self.setCentralWidget(self.widget)
        self.show()

    #check live time
    def time_check(self, time):
        t = time[:2] + time[-2:]
            
        if (int(t) > 500):
            self.on_button_click()
        else:
            QMessageBox.critical(self, "ERROR", "Trains are not operational at entered time.")

    #check if start input is in station (csv)    
    def station_check(self, station0, station1):
        self.csv = csvReader("LondonUndergroundInfo.csv").get_csv()
        s0 = False
        s1 = False

        for i in self.csv:
            if (i[1] == station0 or i[2] == station0):
                s0 = True
            elif (i[1] == station1 or i[2] == station1):
                s1 = True
            else:
                continue
        
        #if input is entered incorrectly
        if (s0 and s1):
            if (self.time.text() == ""):
                self.time_check(self.currentTime[0] + ":" + self.currentTime[1])    
            else:
                self.time_check(self.time.text())
        elif (not s0 and not s1):
            QMessageBox.critical(self, "ERROR", "Stations not found in station list!")
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

    #activates Dijkstra
    #wheelchair feature  
    def on_button_click(self):
        self.wheelchaircsv = csvReader("stationInfo.csv").get_csv()

        if not self.labellist: 
            Dijkstra(self.start.text(), self.currentTime[0] + ":" + self.currentTime[1])
            self.path = Path(self.start.text(), self.end.text())
            print("travel time: ", self.path.get_travel_time(), "mins\n")
            self.ttLabel = QLabel(f"{str(self.path.get_travel_time())} mins total travel time")
            self.ttLabel.setFont(QFont("Comic Sans", 8))
            self.layout1.addWidget(self.ttLabel,len(self.path.get_path()) + 6, 3, 1, 2)
            self.ttLabel.setAlignment(Qt.AlignLeft)
            print("fastest route: ")
            self.drawing()
            for index, i in enumerate(self.path.get_path()):
                print(i)
                if (index == 0):
                    for wheels in self.wheelchaircsv:
                        if (wheels[0] == i and wheels[2] != ""):
                            print(wheels)
                            station = QLabel("♿ " + i, self)
                            station.setFont(QFont("Comic Sans", 8))
                            break
                        else:
                            station = QLabel("      " + i, self)
                            station.setFont(QFont("Comic Sans", 8))

                    station.setStyleSheet("padding: 0 0 0 40")
                    self.labellist.append(station)
                    self.layout1.addWidget(station, int(index + 6), 2)
                else:
                    for wheels in self.wheelchaircsv:
                        if (wheels[0] == i[0] and wheels[2] != ""):
                            print(wheels)
                            station = QLabel("♿ " + i[0], self)
                            station.setFont(QFont("Comic Sans", 8))
                            break
                        else:
                            station = QLabel("      " + i[0], self)
                            station.setFont(QFont("Comic Sans", 8))

                    station.setStyleSheet("padding: 0 0 0 40")
                    self.labellist.append(station)
                    Line = QLabel(i[1], self)
                    Line.setFont(QFont("Comic Sans", 8))
                    self.currentTime[0] + self.currentTime[1]
                    self.labellist.append(Line)
                    totalTravel = QLabel(str(i[3]), self)
                    totalTravel.setFont(QFont("Comic Sans", 8))
                    self.labellist.append(totalTravel)
                    self.layout1.addWidget(station, int(index + 6), 2)
                    self.layout1.addWidget(Line, int(index + 6), 1)
                    Line.setAlignment(Qt.AlignRight)
                    self.layout1.addWidget(totalTravel, int(index + 6), 3)
                    totalTravel.setAlignment(Qt.AlignLeft)

        else: 
            for i in self.labellist:
                self.labellist.remove(i)
                i.clear()
            self.ttLabel.clear()
            self.on_button_click()  

    #displays map of route
    def drawing(self):
        path = self.path.get_path()
        
        self.labeld = QLabel()
        spacing = 15
        rotation = -60
        lineColour = {'Bakerloo':'Brown', 
        'Central': 'Red', 
        'Circle':'Yellow', 
        'District':'Green',
        'Piccadilly':'Dark Blue', 
        'Victoria':'Light Blue', 
        'Hammersmith & City':'Pink',
        'Waterloo & City':'Light Green',
        'Jubilee':'Grey', 
        'Metropolitan':'Purple',
        'Northern':'Black'}

        if (len(path) > self.largestPath):
            self.largestPath = len(path)

        width = spacing  * 2 * self.largestPath + (4 * spacing)
        height = 350

        canvas = QPixmap(width, height)
        canvas.fill(QColor('White'))
        
        
        self.labeld.setPixmap(canvas)
        self.layout1.addWidget(self.labeld, 0, 1, 1, 3)
        painter = QPainter(self.labeld.pixmap())

        
        pen = QPen()
        pen.setWidth(3)
        pen.setColor(QColor('Grey'))
        painter.setPen(pen)

        font = QFont()
        font.setFamily("Comic Sans")
        font.setBold(True)
        font.setPointSize(8)
        painter.setFont(font)

        painter.translate(width // 2, height // 2)

        x1 = -len(path) * spacing - 14.2
        y1 = 8
        x2 = len(path) * spacing - (2 * spacing)
        y2 = 8

        painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        index = 0
        for i in range(-len(path)//2, len(path)//2):
            if index > 0:
                s = path[index][0]
            else:
                s = path[index]

            #draws a colored circle to identify Line 
            painter.save()
            painter.rotate(rotation)
            font.setPointSize(25)
            painter.drawText(int((i * spacing)), int(i * spacing * math.tan(math.radians(60))), s)
            pen.setWidth(15)
            painter.setBrush(Qt.SolidPattern)
            if (index > 0):
                l = path[index][1]
                painter.setPen(QColor(lineColour[l]))
                painter.setBrush(QBrush(QColor(lineColour[l]), Qt.SolidPattern))
            else:
                painter.setPen(QColor("Grey"))
                painter.setBrush(QBrush(QColor("Grey"), Qt.SolidPattern))
            painter.drawEllipse(int((i * spacing) - 14.2), int((i * spacing * math.tan(math.radians(60))) - 3), 9, 9)
            painter.restore()

            index += 1
