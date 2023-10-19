import numpy as np
import sys
import simpy

import LoadData
import dijkstras_algorithm as dji
import contactPlan as cp
import Node

np.set_printoptions(threshold=sys.maxsize)

# Create environment
env = simpy.Environment()

# Create nodes
nodes = []
num_nodes = 66 
zone_radius = 2
for i in range(num_nodes):
    nodes.append(Node.Node(env, i, position=LoadData.get_position_data(i)))

# Initialize an empty adjacency matrix
adjacency_matrix = [np.zeros((num_nodes, num_nodes)) for _ in range(120)]

for node in nodes:
    node.set_all_nodes(nodes)

# Load connections into matrix for entire timeframe
for i in range(120):
    for node in nodes:
        node.findNeighbourNodes(nodes, i)
        for neighbor in node.neighbours:
            adjacency_matrix[i][node.node_id][neighbor.node_id] = 1
            adjacency_matrix[i][neighbor.node_id][node.node_id] = 1  # Since it's an undirected graph


def find_node_by_id(node_id, nodes):
    for node in nodes:
        if node.node_id == node_id:
            return node
    return None  # Node not found



def network_simulator(env, nodes):
    while True:
        # Simulate packet sending process for each node
        contact_plan = cp.generate_contact_plan()

        for contact in contact_plan:
            start_node_id, end_node_id, start_time, end_time = contact
            print(env.now)
            if (start_time == env.now):
                shortest_path = dji.dijkstra(adjacency_matrix[start_time], start_node_id, end_node_id)

                if shortest_path:
                    print(f"Shortest path from node {start_node_id} to node {end_node_id}: {shortest_path}")
                else:
                    print(f"There is no path from node {start_node_id} to node {end_node_id}.")                

                yield env.process(nodes[start_node_id].send_packet(shortest_path))
            else:
                yield env.timeout(1)


# Run the simulation
env.process(network_simulator(env,nodes))
env.run(until=10)