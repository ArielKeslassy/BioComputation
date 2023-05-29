from itertools import combinations, permutations
import networkx as nx


def generate_subgraphs(n):
    """Get all directed, non-isomorphic subgraphs of size n"""

    edges = set()  # Set to store unique edges

    # Generate all possible edges between nodes
    for edge in permutations(range(1, n + 1), 2):
        edges.add(edge)

    subgraphs = []  # List to store the resulting subgraphs

    # Iterate over the number of edges in a subgraph.
    # The number of edges in an undirected bgraph is between n - 1 (in a row) and n(n - 1) (fully connected)
    for i in range(n - 1, (n * (n - 1)) + 1):
        # Generate all combinations of i edges for the subgraph
        for subgraph in combinations(edges, i):
            g = nx.DiGraph()  # Create a directed graph object
            g.add_nodes_from(list(range(1, n + 1)))  # Add nodes to the graph
            g.add_edges_from(subgraph)  # Add edges to the graph

            # Check if the subgraph is connected by converting it to an undirected graph
            if nx.is_connected(g.to_undirected()):
                iso = False  # Flag to check if the subgraph is isomorphic to any existing subgraph

                # Check if the subgraph is isomorphic to any existing subgraph
                for sub in subgraphs:
                    if nx.is_isomorphic(g, sub):
                        iso = True
                        break

                # Add the subgraph to the list if it is not isomorphic to any existing subgraph
                if not iso:
                    subgraphs.append(g)

    return subgraphs


def log_subgraphs(subgraphs, filename, n):
    """Log the subgraphs to a text file"""
    with open(filename, 'w') as f:
        f.write("n={}\n".format(n))
        f.write("count={}\n".format(len(subgraphs)))
        for i, subgraph in enumerate(subgraphs, start=1):
            f.write(f"#{i}\n")
            for edge in subgraph.edges:
                f.write(f"{edge[0]} {edge[1]}\n")

n = 3
x = generate_subgraphs(n)
print(len(x))
log_subgraphs(x, "subgraphs_{}.txt".format(n), n)
