import simpy
import random
from tabulate import tabulate
from math import acos, sin, cos
import distance
import numpy as np
import sys

import LoadData
import dijkstras_algorithm as dji
import contactPlan as cp

np.set_printoptions(threshold=sys.maxsize)

class Node:
    def __init__(self, env, node_id: int, zone_radius: int, neighbours = None, position = None):
        self.env = env
        self.node_id = node_id
        self.zone_radius = zone_radius
        self.routing_table = {}
        self.neighbours = neighbours # List of nodes
        self.packet_queue = simpy.Store(env, capacity=100)
        self.position = position

    def iarp(self):
        # Generate an advertisement packet with TTL = p - 1.

        packet_list = []

        for neighbour in self.neighbours:
            packet = {
                "Type": "ADVERTISEMENT",
                "Node Id": self.node_id,
                "TTL" : zone_radius - 1,
                "Source neighbours": self.neighbours,
                "Path" : [self.node_id],
                "Packet size": 0
            }

            packet_list.append(packet)

        for packet in packet_list:
            self.packet_queue.put(packet)
        
        self.send_packet()
        
        # Append a list of e.g., 2-hop neighbours

    def send_packet(self):
        while True:
            packet = yield self.packet_queue.get()
            packet_type = packet["Type"]
            yield self.env.timeout(random.uniform(0.1, 0.5)) # Simulate transmission

    def receive_packet(self, packet):
        yield self.env.timeout(0) # Process received packet immediately

        # Pass to handler if advertisement packet
        if(packet["Type"] == "ADVERTISEMENT"):
            print(f"Node {self.node_id}: Received ADVERTISMENT")

            # Update path. Note: We only simulate 1 

            packet["Path"].append(self.node_id)

            # If TTL is 0, change packet to ADV Reply and return it
            if (packet["TTL"] == 0):
                packet["Type"] = "ADVERTISEMENT REPLY"
                self.packet_queue.put(packet)
                self.send_packet()
            
            # If not, forward advertisement to neighbours
            else:
                packet["Source neighbours"] = self.neighbours
                packet["TTL"] = packet["TTL"] - 1
                self.packet_queue.put(packet)
                self.send_packet()

        elif(packet["Type"] == "ADVERTISEMENT REPLY"):
            print(f"Node with id {self.node_id}: Received ADVERTISEMENT REPLY")
            path = packet["Path"]

            if(path[0] == self.node_id):
                print(f"Back at origin. Updating routing table")
            else:
                self.packet_queue.put(packet)
                self.send_packet()

    def _handle_advertisement(self, packet):
        """
        Handles advertisements. If TTL == 0 the advertisement is discarded and not forwarded.
        The node appends its ID to the path in order to return a reply to the source node.
        """
        # Update path
        packet["Path"].append(self.node_id)

        # If TTL is 0, change packet to ADV Reply and return to source
        if (packet["TTL"] == 0):
            #print(f"Node with id {self.node_id}: ADVERTISEMENT REPLY")
            packet["Type"] = "ADVERTISEMENT REPLY"
            self.packet_queue.put(packet)
            self.send_packet()
        
        # If not, forward advertisement to neighbours
        else:
            packet["Source neighbours"] = self.neighbours
            packet["TTL"] = packet["TTL"] - 1
            self.packet_queue.put(packet)
            self.send_packet()
    

    def _compare_neighbours(self,source_list):
        source_ids = []
        self_neigbour_ids = []
        for node in source_list:
            source_ids.append(node.node_id)

        for node in self.neighbours:
            self_neigbour_ids.append(node.node_id)

        return source_ids == self_neigbour_ids

    def _receive_advertisement(self, packet):
        yield self.env.timeout(0) # Process received packet immediately
        print(f"Node {self.node_id} received packet: {packet}")


    def update_routing_table(self, destination: int, routes: list, metrics: list):
        # Routing table template
        # [(dest_addr_1, route list, metric list)]
        # Like this: [(1, [1], 5), (2, [1,2], [5, 10]), (3, [1,2,3], [5,10,15])]
        # To access the first item-set: routing_table[0]
        # To access the first item in the first set: routing_table[0][0]

        # Use case:
        #     1. If destination exsits in routing_table: update route + metrics
        #     2. Else add destination, routes, and metics to routing_table

        for i in range(len(self.routing_table)):
            if (self.routing_table[i][0] == destination):
                self.routing_table[i][1] == routes
                self.routing_table[i][2] == metrics

            else:
                self.routing_table.append(destination, routes, metrics)
    

    def get_position_at_time(self, time_index: int):
        series_str = self.position[time_index]
        parts = series_str.split()
        # Check if there are at least two parts (numbers) in the string
        if len(parts) >= 2:
            # Convert the parts to float and create a tuple
            tuple_with_two_numbers = (float(parts[0]), float(parts[1]))
        else:
            print("Not enough numbers in the string to create a tuple")  
        return tuple_with_two_numbers   
    
    def isNeighbourInLOS(self, time_index, neighbour):
        """ Assumes an altitude of 718km """

        self_coordinates = self.get_position_at_time(time_index)
        self_lat = self_coordinates[0]
        self_lon = self_coordinates[1]

        neighbour_coordinates = neighbour.get_position_at_time(time_index)
        neighbour_lat = neighbour_coordinates[0]
        neighbour_lon = neighbour_coordinates[1]

        if (distance.distance(self_lat, self_lon, neighbour_lat, neighbour_lon) < 5000):
            return True
        
        return False

    def findNeighbourNodes(self, nodes, time_index):
        self.neighbours = []
        list = []
        for node in nodes:
            if (node is not self):
                if (self.isNeighbourInLOS(time_index, node)):
                    list.append(node)

        self.neighbours = list




def network_simulator(env, nodes):
    # Simulate packet sending process for each node
    contact_plan = cp.generate_contact_plan()

    for contact in contact_plan:
        start_node, end_node, start_time, end_time = contact
        if (start_time == env.now):
            shortest_path = dji.dijkstra(adjacency_matrix[start_time], start_node, end_node)

            if shortest_path:
                print(f"Shortest path from node {start_node} to node {end_node}: {shortest_path}")
            else:
                print(f"There is no path from node {start_node} to node {end_node}.")

    # Run simulation for 5 time units
    yield env.timeout(10)



# Create environment
env = simpy.Environment()

# Create nodes
nodes = []
num_nodes = 66 
zone_radius = 2
for i in range(num_nodes):
    nodes.append(Node(env, i, zone_radius, position=LoadData.get_position_data(i)))


# Initialize an empty adjacency matrix
adjacency_matrix = [np.zeros((num_nodes, num_nodes)) for _ in range(120)]

# Load connections into matrix for entire timeframe
for i in range(120):
    for node in nodes:
        node.findNeighbourNodes(nodes, i)
        for neighbor in node.neighbours:
            adjacency_matrix[i][node.node_id][neighbor.node_id] = 1
            adjacency_matrix[i][neighbor.node_id][node.node_id] = 1  # Since it's an undirected graph


# Run the simulation
env.process(network_simulator(env,nodes))
env.run(until=10)