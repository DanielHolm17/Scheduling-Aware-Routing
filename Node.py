import simpy
import random
from tabulate import tabulate
from math import acos, sin, cos, sqrt
import distance
import numpy as np

KM_FACTOR = 0.001

class Node:
    def __init__(self, env, node_id: int, position = None):
        self.env = env
        self.node_id = node_id
        self.position = position
        self.nodes = []

    def send_packet(self, path, ETX_values):
        yield self.env.timeout(0.01) # Simulate transmission    
        next_index = path.index(self.node_id)+1
        print(f"Sending packet from node {self.node_id} to node {path[next_index]}")

        # Simulate retransmission
        num_of_retranmission = 0
        retransmit = 1
        while retransmit:
            if (next_index == 1):
                probablity = 1/sqrt(ETX_values[next_index-1])
            else:
                probablity = 1/sqrt((abs(ETX_values[next_index-1] - ETX_values[next_index-2])))

            retransmit = 0 if random.random() < probablity else 1
            if retransmit:
                yield self.env.timeout(0.02)
                print("Retransmission")
                num_of_retranmission += 1

        print(f"Number of retransmissions: {num_of_retranmission}")
        yield self.env.process(self.nodes[path[next_index]].receive_packet(path, ETX_values))
        
    def receive_packet(self, path, ETX_values):
        yield self.env.timeout(0.01) # Process received packet 
        
        if (self.node_id == path[-1]):
            print(f"Transmission complete")
            return
        else:
            yield self.env.process(self.send_packet(path, ETX_values))

    def set_all_nodes(self, nodes):
        self.nodes = nodes

    def get_position_at_time(self, time_index: int):
        series_str = self.position[time_index]
        parts = series_str.split()
        # Check if there are at least two parts (numbers) in the string
        if len(parts) >= 3:
            # Convert the parts to float and create a tuple
            lat_lon_alt = (float(parts[0]), float(parts[1]), float(parts[2]))
        else:
            print("Not enough numbers in the string to create a tuple")  
        return lat_lon_alt
    
    def is_neighbour_in_LOS(self, time_index, neighbour):
        self_coordinates = self.get_position_at_time(time_index)
        self_lat = self_coordinates[0] * KM_FACTOR
        self_lon = self_coordinates[1] * KM_FACTOR
        self_alt = self_coordinates[2] * KM_FACTOR

        neighbour_coordinates = neighbour.get_position_at_time(time_index)
        neighbour_lat = neighbour_coordinates[0] * KM_FACTOR
        neighbour_lon = neighbour_coordinates[1] * KM_FACTOR
        neighbour_alt = neighbour_coordinates[2] * KM_FACTOR

        if (distance.distance(self_lat, self_lon, self_alt, neighbour_lat, neighbour_lon, neighbour_alt) < 5550):
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