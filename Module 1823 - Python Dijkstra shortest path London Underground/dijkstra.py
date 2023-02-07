#https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

from streamlinedDLL import Node, DoublyLinkedList

llist = DoublyLinkedList()

def Dijkstra(source, time, newDist = 0):
    Q = llist.get_all_nodes()
    time = time
    alt = None
    source = llist.find_station(source) #address
    source.dist = newDist
    t = time[:2] + time[-2:]

    if (int(t) >= 900 and int(t) < 1600):
        isFBA = True
    elif (int(t) >= 1900 and int(t) <= 2359):
        isFBA = True
    else:
        isFBA = False

    # while stations are still unvisited - keep running
    while len(Q) > 0:
        # valid station check
        if (source.stationID) not in Q:
            return
        else:
            Q.remove(source.stationID)
            connections = source.connections
            # loop for station connection evaluation
            for i in connections:
                conn_station = llist.find_station(i[0])
                # Bakerloo time check as per coursework specification
                if (isFBA and i[1] == "Bakerloo"):
                    alt = source.dist + (int(i[2]) / 2)
                else:
                    alt = source.dist + int(i[2])
                # if found shorter connection update the distance
                if (alt < conn_station.dist):
                    conn_station.dist = alt
                    conn_station.prev = list((source, i[1], i[2]))
                    Dijkstra(conn_station.stationID, time, conn_station.dist)
