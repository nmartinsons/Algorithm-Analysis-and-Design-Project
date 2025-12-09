import networkx as nx
import matplotlib.pyplot as plt

def forms_cycle(mst, src, dest):
    if not mst:
        return False
    # Adjacency list (graph map) for the current MST
    graph = {}
    for u, v, w in mst:
        if u not in graph:
            # Creating empty list for adjacency for source if not present
            graph[u] = []
        if v not in graph:
                # Creating empty list for adjacency for destination if not present
            graph[v] = []
        # Creating a link in both directions since it's an undirected graph
        graph[u].append(v)
        graph[v].append(u)
    # If either src or dest is not in the graph, no cycle can be formed 
    if src not in graph or dest not in graph:
        return False
    
    # Perform DFS to find a path (Iterative approach)
    # DFS is efficient for simply checking for thing connectedness
    visited = set()
    # Stack for DFS, initialized with the source node
    stack = [src]
    # As long as there are nodes to explore
    while stack:
        # Pop a node from the stack, LIFO order
        node = stack.pop()
        # If we reached the destination node
        if node == dest:
            return True # Path exists, cycle would be formed
        # If the node has not been visited yet
        if node not in visited:
            # Mark the node as visited, safe operation, it means nodes are disonnected
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)
                    
    return False # No cycle detected

edges = [] # To store edges as src, dest, and weight
G_original = nx.Graph() # To store the "Before" state

# Reading the CSV file and constructing the edge list
with open("../actual_distances_space_graph.csv", "r") as file:
    lines = file.readlines()

    # Skip the header
    for line in lines[1:]:
        # Split the line into parts based on comma
        parts = line.strip().split(',')
        src = parts[0].strip()      # Column 0: Source
        dest = parts[1].strip()    # Column 1: Destination
        # Column 2: distanceLY
        weights = float(parts[2]) 
        # Handling zero weights by assigning a small value
        if weights == 0:
            weights = 0.000001 
        
        # Kruskle's Algorithm Implementation
        edges.append((src, dest, weights))
        # Adding edges to the original graph for "Before" visualization
        G_original.add_edge(src, dest, weight=weights)


# 1. Sorting edges in increasing order of weights
sorted_edges = sorted(edges, key=lambda x: x[2])

# 2. Empty graph to store the MST
mst = []
# Total weight of the MST
total_weight = 0
# To store the "After" state
G_mst = nx.Graph()

# 3. Iterating through sorted edges and adding them to the MST if they don't form a cycle
for sorted_edge in sorted_edges:
    src, dest, weight = sorted_edge
    # If adding the edge to the subgraph does not create a cycle, add it to the subgraph
    # If adding the edge to the subgraph creates a cycle, discard it and move on to the next edge
    if not forms_cycle(mst, src, dest):
        mst.append((src, dest, weight))
        total_weight += weight
        # Adding to MST Graph object
        G_mst.add_edge(src, dest, weight=weight)
        print(f"Added edge: {src} -> {dest} ({weight})")
print(f"Total MST Weight: {total_weight:.2f}")

# Visualization of Before and After MST
G = nx.Graph()
for u, v, w in mst:
    G.add_edge(u, v, weight=w)
    
# Separates nodes perfectly without overlapping
pos = nx.spring_layout(G_original, k=0.5, weight=None, seed=42)

# Window for side by side comparison
plt.figure(figsize=(16, 8))

# Before MST
plt.subplot(1, 2, 1)
plt.title("Original Graph", fontsize=14)
nx.draw(G_original, pos, 
        with_labels=True, 
        node_color='lightblue', 
        node_size=2000, 
        font_size=10, 
        font_weight='bold')
# Drawing the Edge Weights
edge_labels_original = nx.get_edge_attributes(G_original, 'weight')
nx.draw_networkx_edge_labels(G_original, pos, edge_labels_original, font_size=8)

# After MST
plt.subplot(1, 2, 2)
plt.title("Minimum Spanning Tree", fontsize=14)
nx.draw(G, pos, 
        with_labels=True, 
        node_color='green', 
        node_size=2000, 
        font_size=10, 
        font_weight='bold')
# Drawing the Edge Weights
edge_labels_mst = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G_mst, pos, edge_labels_mst, font_size=8)

# Fixes the layout and spacing issues
plt.tight_layout()
# Showing the plot
plt.show()       