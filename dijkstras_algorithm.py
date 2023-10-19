import heapq

def dijkstra(graph, start, end):
    previous_nodes = [None] * len(graph)

    # Initialize distances to all nodes as infinity, except for the start node (distance is 0)
    distances = [float('inf')] * len(graph)
    distances[start] = 0
    
    # Priority queue to keep track of the nodes to visit
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # If we have reached the end node, we have found the shortest path
        if current_node == end:
            path = []
            while current_node is not None:
                path.insert(0, current_node)
                current_node = previous_nodes[current_node]
            return path
        
        # Skip nodes that have already been visited
        if current_distance > distances[current_node]:
            continue
        
        # Explore the neighbors of the current node
        for neighbor, weight in enumerate(graph[current_node]):
            if weight == 1:  # Assuming unweighted graph
                distance = current_distance + 1  # Weight of 1 for unweighted edges
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))
    
    # If we reach this point, there is no path from start to end
    return []