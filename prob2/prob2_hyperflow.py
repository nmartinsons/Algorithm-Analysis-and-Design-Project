import networkx as nx
import matplotlib.pyplot as plt

def bfs(src, sink, parent, graph):
    # Visited set to keep track of visited nodes
    visited = set()
    # Queue to store nodes for BFS
    queue = []
    
    # Start BFS from the source node
    queue.append(src)
    # Mark the source node as visited
    visited.add(src)
    # Parent of source is None, clear previous path
    parent.clear()
    
    # BFS Loop
    # u is the First Node (Start)
    # v is the Second Node (End)
    while queue:
        u = queue.pop(0) # Remove element from front of the queue
        
    for v in graph[u]:
        # If the node has not been visited and there is available capacity
        if v not in visited and graph[u][v]>0:
            queue.append(v)
            visited.add(v)
            # Set parent for path reconstruction
            parent[v] = u
            if v == sink:
                return True
            
  
def max_flow_ford(graph, src, sink):
    max_flow = 0
    parent = {}
    # Copy the original graph to residual graph
    # v represents the entire dictionary of neighbors and their capacities and we copy it
    # u assigns each key to its own copy of the neighbor dictionary
    res_graph = {u: v.copy() for u, v in graph.items()}
    
    # While there is a path from source to sink with available capacity
    while bfs(src, sink, parent, res_graph):
        path_flow = float("Inf")
        v = sink
        # Find the maximum flow through the path found by BFS, while backtracking from sink to source
        while v != src:
            # u is the parent of v
            u = parent[v]
            # The availeble capacity on the edge u->v
            path_flow = min(path_flow, res_graph[u][v])
            # Check edge from u to v, when v is src, the loop ends
            v = u
        # Adding the path flow to overall flow
        max_flow += path_flow
        
        # Updating the residual graph capacities of the edges and reverse edges along the path
        v = sink
        while v != src:
            u = parent[v]
            res_graph[u][v] -= path_flow
            # Reverse path
            # Ensure the reverse adjacency dict exists for node v
            if v not in res_graph:
                res_graph[v] = {}
            # Ensure the reverse edge v->u exists (initialize to 0 if missing)
            if u not in res_graph[v]:
                res_graph[v][u] = 0
            # Reversing the flow
            res_graph[v][u] += path_flow
            v = u
    return max_flow, res_graph

#  Dict of dict to represent the adjacency list with capacities
adjacency_list = {}
edges = []
      
with open("../actual_distances_space_graph.csv", "r") as file:
    lines = file.readlines()

    # Skip the header
    for line in lines[1:]:
        # Split the line into parts based on comma
        parts = line.strip().split(',')
        src = parts[0].strip()     # Column 0: Source
        dest = parts[1].strip()     # Column 1: Destination
        # Column 3: hyperflowSpiceMegaTons
        flow = float(parts[3]) 
        
        if src not in adjacency_list: adjacency_list[src] = {}
        if dest not in adjacency_list: adjacency_list[dest] = {}
        
        # Directed graph, so only one direction and store capacity
        adjacency_list[src][dest] = flow
        
        # For storing edges for later use (visualization)
        edges.append((src, dest, flow))
       
        print(f"Edge: {src} -> {dest} ({flow})")
        
src_node = "Earth"
sink_node = "Betelgeuse"

tot_flow, res_graph = max_flow_ford(adjacency_list, src_node, sink_node)
print(f"Total Maximum Hyperflow from {src_node} to {sink_node}: {tot_flow}")

# Visualization of the graph with capacities
G = nx.DiGraph()

# Outer loop to go through each node and its neighbors
for u, neighbors in adjacency_list.items():
    # Inner loop to go through each neighbor and its capacity
    for v, capacity in neighbors.items():
        # Check remaining capacity in residual graph
        remaining_capacity = res_graph[u][v]
        # Claculating used capacity
        used_capacity = capacity - remaining_capacity
        
        if capacity > 0:
            # Format the label to show used/total capacity
            label = f"{int(used_capacity)}/{int(capacity)}"
            
            G.add_edge(u, v, label=label)
    
plt.figure(figsize=(12, 8))      
pos = nx.kamada_kawai_layout(G)

nx.draw_networkx_nodes(G, pos, node_size=800, node_color='lightgrey')
nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold")


nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20)


# Draw Labels (Flow / Capacity)
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

plt.title(f"Max Flow Visualization ({src_node} -> {sink_node})")
plt.show()

    
    