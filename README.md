# Module-1823-Python-Dijkstra-shortest-path-London-Underground

This is uploaded for posterity.

2nd year university project.

No mapping data structures were allowed to be used, only the doubly-linked list.
The algorithm is no where close to efficient, owing to the constraints.

The idea was find the departure station & then perform a dijktra shortest path algorithm until the destination station is found.
While looking for the destination station, the stations encounted along the way are added as forward connections in the doubly-linked list from the departure station.
If a shorter path is found to a station along the way, the reverse connection is updated from that station to the station with the shortest path.

This allows all stations within the network to have a reverse attribute that will point back to the departure station, once the djiksta algorithm has been run, along the shortest path. And for all stations that can be visited 1 step away from the current station to be accessible by the foward attribute.

Improvements would include a data structure that compliments the scenario, a heuristic pathing algorithm, potential checks for the destination station already being on the same line as the departure station.
Improvements inline with the contraints would include code readability, the project had no strucure and was largely figured out line by line.
