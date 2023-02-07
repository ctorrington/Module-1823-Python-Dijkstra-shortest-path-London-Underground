from csvReader import *
import math

csv = csvReader("LondonUndergroundInfo.csv").get_csv()

# Node class for each station
class Node:  
    def __init__(self, data): 
        self.stationID = data
        self.next = None
        self.prev = None

        self.connections = list()
        self.dist = math.inf

# data structure for storing node class
class DoublyLinkedList:
    def __init__(self): 
        self.head = None
        self._setup()

    def _setup(self):
        self._create_nodes()
        self._create_connections()

    def _create_nodes(self):
        self.added = []
        for i in csv:
            if i[1] not in self.added:
                self._append_node(i[1])
                self.added.append(i[1])
            if i[2] not in self.added:
                self._append_node(i[2])
                self.added.append(i[2])

    def _create_connections(self):
        for i in csv:
            self._append_connection(list((i[1], i[2], i[0], i[3])))
            self._append_connection(list((i[2], i[1], i[0], i[3])))

    def _append_node(self, new_data):
        self.new_node = Node(new_data) 
        self.new_node.next = None

        if self.head is None:
            self.new_node.prev = None
            self.head = self.new_node 
            return
  
        self.last = self.head 
        while(self.last.next is not None): 
            self.last = self.last.next
  
        self.last.next = self.new_node 
        return

    def _append_connection(self, connectionInfo):
        self.current = self.head
        while self.current is not None:
            if self.current.stationID == connectionInfo[0]:
                self.current.connections.append(list((connectionInfo[1], connectionInfo[2], connectionInfo[3]))) #<- everything at this point should be unique
            self.current = self.current.next

    def find_station(self, stationInfo):
        self.current = self.head
        while self.current is not None:
            if self.current.stationID == stationInfo:
                return self.current
            else:
                self.current = self.current.next

    # used for debugging
    def print_dll(self):
        self.station = self.head
        while self.station is not None:
            print("station: ", self.station.stationID)
            print("connections: ", self.station.connections)
            self.station = self.station.next

    def get_all_nodes(self):
        self.station = self.head
        nodes = list()
        while self.station is not None:
            nodes.append(self.station.stationID)
            self.station = self.station.next
        return nodes

    def get_connections(self, stationInfo: list):
        self.station = self.find_station(stationInfo)
        return self.station.connections

    # return a list of the stations along the route determined by dijkstras algorithm
    def get_route(self, start, end):
        self.station = self.head
        self.start = self.find_station(start).stationID
        self.end = self.find_station(end).stationID
        self.route = list()

        while self.station.stationID != end:
            self.station = self.station.next
        while self.station.stationID != start:
            self.route.append(list((self.station.stationID, self.station.prev[1], self.station.dist)))
            self.station = self.station.prev[0]

        self.route.append(self.station.stationID)
        self.route.reverse()
        return self.route

    def get_dist(self, station):
        self.station = self.find_station(self.station)
        return self.station.dist

    def set_dist(self, stationInfo, distance):
        self.find_station(stationInfo).dist = distance
