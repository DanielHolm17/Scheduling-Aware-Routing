import numpy as np
import sys
import simpy
import pandas as pd
from scipy.stats import halfnorm

import LoadData
import dijkstras_algorithm as dij
import planned_transmissions as pt
import Node
import Node_zrp

######## Helper functions ###########

def find_node_by_id(node_id, nodes):
    for node in nodes:
        if node.node_id == node_id:
            return node
    return None  # Node not found

def sort_table(table):
    sorted_routing = sorted(table.items())
    return dict(sorted_routing)

def find_node_neighbours(nodes: [], index : int):
    for node in nodes:
        node.find_neighbour_nodes(nodes, index)
        node.set_all_nodes(nodes)

def get_ETX_from_ZRP_nodes(node1_id : int, node2_id : int):
    for zrp_node in zrp_nodes:
        if (zrp_node.node_id == node1_id):
            for key, route in zrp_node.metrics_table.items():
                if (key == node2_id):
                    for sublist in route:
                        if (len(sublist) == 1):
                            return sublist[0]

def generate_adjacency_matrix():
    # Load connections into matrix for entire timeframe
    for i in range(run_time):
        for node in nodes:
            node.find_neighbour_nodes(nodes,i)
            for neighbor in node.neighbours:
                #if (adjacency_matrix[i][node.node_id][neighbor.node_id] != 0):     # Already data here 
                #    continue

                random_value = get_ETX_from_ZRP_nodes(node.node_id, neighbor.node_id)         
                adjacency_matrix[i][node.node_id][neighbor.node_id] = random_value
                #adjacency_matrix[i][neighbor.node_id][node.node_id] = random_value # Since it's an undirected graph


# Create environment
env = simpy.Environment()
num_nodes = 30
run_time = 120
sample_time = 1

# Create ZRP nodes to get the same ETX values
zrp_nodes = []
zone_radius = 1
for i in range(num_nodes):
    zrp_nodes.append(Node_zrp.Node(env, i, zone_radius, position=LoadData.get_position_data(i)))

# Create nodes
nodes = []
for i in range(num_nodes):
    nodes.append(Node.Node(env, i, position=LoadData.get_position_data(i)))
for node in nodes:
    node.set_all_nodes(nodes)

# Initialize an empty adjacency matrix
adjacency_matrix = [np.zeros((num_nodes, num_nodes)) for _ in range(120)]


def IARP_process(env):
    np.random.seed(41)
    find_node_neighbours(zrp_nodes, 0)
    
    for node in zrp_nodes:
            packet_count = 0
            node.routing_table_new.clear()
            node.metrics_table_new.clear()
            node.paths_to_destinations.clear()
            yield env.process(node.iarp())
            node.routing_table = node.routing_table_new
            node.metrics_table = node.metrics_table_new

            node.routing_table = sort_table(node.routing_table)
            node.metrics_table = sort_table(node.metrics_table)

def network_simulator(env, nodes):
    #planned_tranmission = pt.generate_planned_transmission()
    planned_tranmission = [(0, 7, 0), (2, 26, 5), (22, 11, 11), (15, 8, 17), (27, 20, 23)]

    yield env.process(IARP_process(env))        # Create routing table for node
    generate_adjacency_matrix()                 # Create adjacency matrix

    df = pd.DataFrame(adjacency_matrix[0])
    df.to_excel('adjacency_matrix_0.xlsx')

    for i in range(run_time):
        for tranmission in planned_tranmission:
            start_node_id, end_node_id, start_time = tranmission

            if (start_time == env.now):
                shortest_path, distance = dij.dijkstra(adjacency_matrix[start_time], start_node_id, end_node_id)

                if shortest_path:
                    print(f"Best path from node {start_node_id} to node {end_node_id}: {shortest_path}")
                else:
                    print(f"There is no path from node {start_node_id} to node {end_node_id}.")                

                planned_tranmission.pop(planned_tranmission.index(tranmission))
                yield env.process(nodes[start_node_id].send_packet(shortest_path, 0, distance))

        yield env.timeout(1)

# Run the simulation
env.process(network_simulator(env,nodes))
env.run()