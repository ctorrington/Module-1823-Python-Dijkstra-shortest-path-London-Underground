from main import *
from random import randrange

# this class processes the raw travel time from dijkstra and adds the waiting time between stations
class Path:
    def __init__(self, start, destination):
        self._disembarkment = 0
        self._travelTime = 0
        self._route = llist.get_route(start, destination)
        self._path = list()

        # enumerating over total travel time along the _route
        for index, i in enumerate(self._route):
            if ((isinstance(i[2], float)) or (isinstance(i[2], int))):
                # +1 for the disembarking of passengers
                # +rand(0-5) 'simulating' waiting for anouther train from a different line
                self._disembarkment += 1 + self.check_line_change(i[1], self._route[index-1][1])
                self._travelTime = int(i[2]) + self._disembarkment
                i.append(self._travelTime)
                self._path.append(i)
            else:
                self._path.append(i)
    
    # as per coursework specification, simulating trains departing every 5 min
    def check_line_change(self, line, prev = None):
        if (line == prev):
            return 0
        else:
            if (isinstance(prev, int)):
                return randrange(0, 5)
            else:
                return 0

    def get_path(self):
        return self._path

    def get_travel_time(self):
        return self._travelTime
