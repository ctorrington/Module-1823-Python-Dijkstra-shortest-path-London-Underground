import sys
from csv import *
from path import *
from dijkstra import *
from csvReader import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import datetime
from guipt2 import *

class uiBackend():
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