import heapq

def dijkstra(graph, start, end):
    previous_nodes = [None] * len(graph)
    ETX = [None] * len(graph)

    # Initialize distances to all nodes as infinity, except for the start node (distance is 0)
    distances = [float('inf')] * len(graph)
    distances[start] = 0
    
    # Priority queue to keep track of the nodes to visit
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        print(f"Searched nodes {current_node}")
        
        # If we have reached the end node, we have found the shortest path
        if current_node == end:
            path = []
            distance = []
            while current_node is not None:
                path.insert(0, current_node)
                if (ETX[current_node] != None):
                    distance.insert(0, ETX[current_node])
                current_node = previous_nodes[current_node]
            return path, distance
        
        # Skip nodes that have already been visited
        if current_distance > distances[current_node]:
            continue
        
        # Explore the neighbors of the current node
        for neighbor, weight in enumerate(graph[current_node]):
            if weight == 0:
                continue    # Skip invalid connections
            
            distance = current_distance + (1/weight**2)        # Calculate ETX for each hop and add to distance 
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                ETX[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    # If we reach this point, there is no path from start to end
    return []