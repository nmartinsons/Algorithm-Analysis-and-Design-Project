# Longest Shortest Path (Diameter): The maximum distance required to traverse the network, provided you take the best route.

import networkx as nx
import matplotlib.pyplot as plt

#  First, computing shortest paths using Floyd-Warshall Algorithm 
def floyd_warshall_algo(graph, nodes):
    # Initialize distance matrix for every node to every other node
    dist = {u: {v: float('inf') for v in nodes} for u in nodes}
    for u in nodes:
        dist[u][u] = 0 # Distance to self is zero
    for u in graph:
        for v in graph[u]:
            # Loading direct weights in the distance matrix
            dist[u][v] = graph[u][v] # Direct edge weight
            dist[v][u] = graph[u][v] # Undirected graph
    # k is the intermediate node
    # i is the source node
    # j is the destination node
    for k in nodes:
        for i in nodes:
            for j in nodes:
                # If a shorter path is found via k, update the distance
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

adjacency_list = {}
# For avoiding duplicate nodes
nodes_set = set()

# Reading the CSV file and constructing the edge list
with open("../actual_distances_space_graph.csv", "r") as file:
    lines = file.readlines()

    # Skip the header
    for line in lines[1:]:
        # Split the line into parts based on comma
        parts = line.strip().split(',')
        src = parts[0].strip()      # Column 0: Source
        dest = parts[1].strip()     # Column 1: Destination
        # Column 2: distanceLY
        weights = float(parts[2]) 
        # Handling zero weights by assigning a small value
        if weights == 0:
            weights = 0.000001
        
        # Adding to the nodes set 
        nodes_set.add(src)
        nodes_set.add(dest)
        
        # Adjacency list construction for undirected graph
        if src not in adjacency_list: adjacency_list[src] = {}
        if dest not in adjacency_list: adjacency_list[dest] = {}
        
        # Adding the edge in both directions
        adjacency_list[src][dest] = weights
        adjacency_list[dest][src] = weights
        
all_pairs_shortest_paths = floyd_warshall_algo(adjacency_list, list(nodes_set))

# Finding the diameter (longest shortest path)
diameter = 0
for u in all_pairs_shortest_paths:
    for v in all_pairs_shortest_paths[u]:
        distance = all_pairs_shortest_paths[u][v]
            # If we found a new record...
        if distance != float('inf') and distance > diameter:
            # Update the number for diameter, the longest shortest path found so far
            diameter = distance 
            # Update the context for start and end nodes
            start_node = u
            end_node = v
print(f"Diameter of the Space Graph: {diameter} light years, between {start_node} and {end_node}")

# Visualization of the graph with found diameter
G = nx.Graph()
# Adding edges to the graph for visualization
for u in adjacency_list:
    for v in adjacency_list[u]:
        G.add_edge(u, v, weight=adjacency_list[u][v])

#  Getting the path corresponding to the diameter, using built-in shortest path function from NetworkX
path_nodes = nx.shortest_path(G, source=start_node, target=end_node, weight='weight')
# Creating edge list for the path, 1: slicing makes sure that we pair node with its neighbor node
# zip creates pairs of (node, next_node)
path_edges = list(zip(path_nodes, path_nodes[1:]))
        
plt.figure(figsize=(12, 8))

# Drawing the graph
pos = nx.spring_layout(G, k=1.5, weight=None, seed=42)

# Firs layer: all nodes and edges in light grey
nx.draw_networkx_nodes(G, pos, node_color='lightgrey', node_size=700)
nx.draw_networkx_edges(G, pos, edge_color='lightgrey')
nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold")

# Second layer: highlight the diameter path in RED color
nx.draw_networkx_nodes(G, pos, nodelist=path_nodes, node_color='red', node_size=700)
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

edge_labels = nx.get_edge_attributes(G, 'weight')

nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

plt.title(f"Diameter: {diameter:.2f} LY ({start_node} -> {end_node})")
plt.show()  
  

    