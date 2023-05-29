# Gene Regulatory Network Motifs Generator
This Python code generates all the directed, non-isomorphic subgraphs of a given size, representing the possibilities for motifs on Gene Regulatory Networks (GRN). Gene Regulatory Networks are complex systems that control the expression of genes in living organisms. Understanding the motifs, which are recurring patterns of interactions between genes, is crucial for unraveling the underlying regulatory mechanisms.

## Motifs and Subgraphs
Motifs in GRNs refer to specific patterns of gene interactions that occur frequently across different organisms. They are considered building blocks of regulatory networks and play important roles in various biological processes such as development, cell differentiation, and response to environmental cues.

In this code, motifs are represented as directed subgraphs, where the nodes correspond to genes, and the edges represent regulatory interactions between genes. The code generates all possible subgraphs of a given size that are non-isomorphic, meaning they are structurally distinct from each other. Each subgraph represents a unique motif configuration that can be observed in Gene Regulatory Networks.

## Code Functionality
The code utilizes the networkx library to create and manipulate directed graphs. It employs combinatorial techniques from the itertools module to generate all possible edges and combinations for constructing subgraphs. The following steps outline the functionality of the code:
- Generation of Edges: All possible edges between nodes are generated using permutations, ensuring uniqueness and proper ordering.
- Subgraph Generation: The code iterates over the number of edges in a subgraph, generating all combinations of edges for each size. For each combination, a directed graph object is created using networkx. Nodes are added to the graph, and the corresponding edges are added based on the combination.
- Subgraph Filtering: The code checks if the generated subgraph is connected by converting it to an undirected graph and using the is_connected function from networkx. It also verifies if the subgraph is isomorphic to any existing subgraphs to ensure non-redundancy and uniqueness.
- Logging Subgraphs: A logging function is provided to write the generated subgraphs to a text file. The subgraphs are logged in a specified format, with each subgraph denoted by an index and its edges listed below.

# Usage
To use the code, simply call the generate_subgraphs function, providing the desired size of the subgraphs (motifs) as an argument. The function will return a list of non-isomorphic subgraphs. You can then use the log_subgraphs function to log the subgraphs to a text file for further analysis.

python code:
```
n = 3
x = generate_subgraphs(n)
log_subgraphs(x, "subgraphs{}.txt".format(n), n)
```
