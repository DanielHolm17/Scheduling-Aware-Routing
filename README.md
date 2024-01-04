# Scheduling-Aware-Routing
Python implementation for Scheduling Aware Routing for a satellite network. 

## Nodes 
The code consist of two classes called Node and Node_zrp. The Node_zrp is only there to get the same ETX values as used in ZRP, and is a copy from the ZRP repository here: https://github.com/mathias-magnusson/Zone-routing-protocol
The Node class consists of all the nodes in the network and is created in main. The num_nodes variable is used to changed the node population to: 66, 132, 264, 396, or 528.

The nodes are capable of sending and receiving packets, and can simulate retransmissions based on the ETX values given.

## Main
In main the adjacency matrix is created based on the num_nodes and the amount of samples. It is being loaded with ETX values from the Node_zrp nodes.

## Simulation 
When main is run the simulation is started. It looks at the planned_transmission and checks whether it is time to create a route or not. The planned_transmissions can be generated at random with generate_planned_transmission() or it can be set manually. 
When it is time to create a route, Dijkstra's algorithm is used, which returns the best route and the accumulated ETX cost for each hop.
This data is used when the packet is being sent, where the ETX value can be changed with ETX_for_route_changed(). 
