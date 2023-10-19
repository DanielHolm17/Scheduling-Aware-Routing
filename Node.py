import simpy
import random
from tabulate import tabulate
from math import acos, sin, cos
import distance

class Node:
    def __init__(self, env, node_id: int, position = None):
        self.env = env
        self.node_id = node_id
        self.routing_table = {}
        self.position = position
        self.nodes = []

    def send_packet(self, path):
        yield self.env.timeout(1) # Simulate transmission        
        next_index = path.index(self.node_id)+1

        print(f"Sending packet from node {self.node_id} to node {path[next_index]}")
        self.env.process(self.nodes[path[next_index]].receive_packet(path))
        
    def receive_packet(self, path):
        yield self.env.timeout(1) # Process received packet 

        if (self.node_id == path[-1]):
            print("Transmission complete")
            return
        else:
            self.env.process(self.send_packet(path))

    def set_all_nodes(self, nodes):
        self.nodes = nodes

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