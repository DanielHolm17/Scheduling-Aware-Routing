import simpy
import random
from tabulate import tabulate
from math import acos, sin, cos
import distance

class Node:
    def __init__(self, env, node_id: int, position = None):
        self.env = env
        self.node_id = node_id
        self.position = position
        self.nodes = []
        self.transmission_time = 0

    def send_packet(self, path, transmission_time):
        yield self.env.timeout(0) # Simulate transmission    
        transmission_time += 1

        next_index = path.index(self.node_id)+1

        print(f"Sending packet from node {self.node_id} to node {path[next_index]}")
        self.env.process(self.nodes[path[next_index]].receive_packet(path, transmission_time))
        
    def receive_packet(self, path, transmission_time):
        yield self.env.timeout(0) # Process received packet 
        transmission_time += 1

        if (self.node_id == path[-1]):
            print(f"Transmission complete - time: {transmission_time}")
            return
        else:
            self.env.process(self.send_packet(path, transmission_time))

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
    
    def is_neighbour_in_LOS(self, time_index, neighbour):
        """ Assumes an altitude of 718km """

        self_coordinates = self.get_position_at_time(time_index)
        self_lat = self_coordinates[0]
        self_lon = self_coordinates[1]

        neighbour_coordinates = neighbour.get_position_at_time(time_index)
        neighbour_lat = neighbour_coordinates[0]
        neighbour_lon = neighbour_coordinates[1]

        if (distance.distance(self_lat, self_lon, neighbour_lat, neighbour_lon) < 6000):
            return True
        
        return False

    def find_neighbour_nodes(self, nodes, time_index):
        self.neighbours = []
        list = []
        for node in nodes:
            if (node is not self):
                if (self.is_neighbour_in_LOS(time_index, node)):
                    list.append(node)

        self.neighbours = list