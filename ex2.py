from itertools import combinations
import networkx as nx


def graph_partitioning(n, g):
    """Partition a directed graph into a list of subgraphs that contain non-isomorphic subgraphs of size n
    :param n: size of the subgraphs
    :param g: nx.DiGraph object
    :return: list of subgraphs
    """
    node_combinations = g.nodes()
    subgraphs = []
    for i in range(1, len(node_combinations) + 1):
        for combination in combinations(node_combinations, i):
            subgraph = g.subgraph(combination)
            if len(subgraph) == n:
                subgraphs.append(subgraph)
    # return as a list of tuples
    subgraphs = [g.edges for g in subgraphs]
    return subgraphs


def count_motifs_repetitions(subgraphs):
    """Count the number of repetitions of each motif in the list of subgraphs
    :param subgraphs: list of subgraphs
    :return: dictionary of motifs and their counts
    """
    unique_motifs = dict.fromkeys(subgraphs, 1)
    for g, h in combinations(subgraphs, r=2):
        if nx.is_isomorphic(g, h):
            unique_motifs[g] += 1
            unique_motifs.pop(h)

    return unique_motifs


def generate_motifs(n, e):
    """
    Generate all motifs of size n in graph g into a .txt file
    :param n: size of the motifs
    :param g: list of edges in the graph
    :return: None
    """

    # Create a directed graph object
    graph = nx.DiGraph(e)

    subgraphs = [nx.DiGraph(list(tuple(g))) if len(g) != 1 else nx.DiGraph(list((tuple(g))))
                 for g in graph_partitioning(n, graph)]

    unique_motifs_dict = count_motifs_repetitions(subgraphs)

    # Write the subgraphs to a text file
    with open("motifs_{}.txt".format(n), 'w') as f:
        f.write("n={}\n".format(n))
        for i, (subgraph, count) in enumerate(unique_motifs_dict.items(), start=1):
            f.write("count={}\n".format(count))
            f.write(f"#{i}\n")
            for edge in subgraph.edges:
                f.write(f"{edge[0]} {edge[1]}\n")


# Generate all motifs of size n in the graph
n = 3
generate_motifs(3, [(2, 1), (4, 2), (3, 1), (4, 3)])
