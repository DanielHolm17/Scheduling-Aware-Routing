import numpy as np
import sys
import simpy

import LoadData
import dijkstras_algorithm as dji
import planned_transmissions as pt
import Node
from scipy.stats import halfnorm

np.set_printoptions(threshold=sys.maxsize, linewidth=150, precision=3)

def find_node_by_id(node_id, nodes):
    for node in nodes:
        if node.node_id == node_id:
            return node
    return None  # Node not found

# Create environment
env = simpy.Environment()

# Create nodes
nodes = []
num_nodes = 66
for i in range(num_nodes):
    nodes.append(Node.Node(env, i, position=LoadData.get_position_data(i)))

for node in nodes:
    node.set_all_nodes(nodes)

# Initialize an empty adjacency matrix
adjacency_matrix = [np.zeros((num_nodes, num_nodes)) for _ in range(120)]

run_time = 120
sample_time = 1

# Load connections into matrix for entire timeframe
for i in range(run_time):
    for node in nodes:
        node.find_neighbour_nodes(nodes,i)
        for neighbor in node.neighbours:
            if (adjacency_matrix[i][node.node_id][neighbor.node_id] != 0):     # Already data here 
                continue

            half_normal_data = halfnorm.rvs(size=1)
            # Apply a power transformation with a negative exponent
            power_parameter = -3
            transformed_data = 1 - np.exp(power_parameter * half_normal_data)
            
            adjacency_matrix[i][node.node_id][neighbor.node_id] = transformed_data[0]
            adjacency_matrix[i][neighbor.node_id][node.node_id] = transformed_data[0] # Since it's an undirected graph

def network_simulator(env, nodes):
    planned_tranmission = pt.generate_planned_transmission()
    planned_tranmission = list(planned_tranmission)

    for tranmission in planned_tranmission:
        node1, node2, start_time = tranmission
        print(f"Node {node1} sending to {node2} at time {start_time}")

    for i in range(run_time): 
        for tranmission in planned_tranmission:
            start_node_id, end_node_id, start_time = tranmission

            if (start_time == env.now):
                shortest_path, distance = dji.dijkstra(adjacency_matrix[start_time], start_node_id, end_node_id)
                print(distance)
                if shortest_path:
                    print(f"Shortest path from node {start_node_id} to node {end_node_id}: {shortest_path}")
                else:
                    print(f"There is no path from node {start_node_id} to node {end_node_id}.")                

                planned_tranmission.pop(planned_tranmission.index(tranmission))
                yield env.process(nodes[start_node_id].send_packet(shortest_path, 0))

        yield env.timeout(1)


# Run the simulation
env.process(network_simulator(env,nodes))
env.run()