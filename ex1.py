import time
from itertools import combinations, permutations
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


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


def runtime_equation(n, a, b, c):
    """Equation to estimate runtime based on input size"""
    return a * np.exp(b * n) + c


def format_runtime(runtime):
    """Convert runtime to hours if greater than 200 seconds"""
    if runtime > 200:
        return f"{runtime / 3600:.2f} hours"
    else:
        return f"{runtime:.2f} sec"


def plotData(n_values_arr, runtimes_arr, predict_n_values):
    """Plot the runtime analysis graph and predicted runtimes"""

    # Perform curve fitting to estimate the equation
    popt, pcov = curve_fit(runtime_equation, n_values_arr, runtimes_arr, maxfev=10000)

    # Generate predicted runtimes using the fitted equation
    predicted_runtimes = runtime_equation(predict_n_values, *popt)

    # Extend the y-axis limits up to 8 hours (28800 seconds)
    y_max = max(max(runtimes_arr), 28800)

    # Set the desired figure size
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the graph
    ax.plot(n_values_arr, runtimes_arr, 'bo-', label='Actual Runtimes')
    ax.plot(predict_n_values, predicted_runtimes, 'ro-', label='Predicted Runtimes')

    # Add runtime values as text on the plot
    for i in range(len(n_values_arr)):
        plt.text(n_values_arr[i], runtimes_arr[i], f"{runtimes_arr[i]:.2f}", ha='center', va='bottom')
    for i in range(len(predict_n_values)):
        plt.text(predict_n_values[i], predicted_runtimes[i], f"{predicted_runtimes[i]:.2f}", ha='center', va='bottom')

    plt.ylim(0, y_max)
    plt.xlabel('n values')
    plt.ylabel('Runtime (in sec)')
    plt.title('Runtime Analysis of generating the subgraphs')
    plt.legend()

    # Create the equation string
    if popt[0] > 0.001:
        equation_string = f"Equation: {popt[0]:.2f} * exp({popt[1]:.2f} * n)"
    else:
        equation_string = f"Equation: exp({popt[1]:.2f} * n)"

    # Add the equation as text on the plot
    plt.text(0.02, 0.98, equation_string, transform=plt.gca().transAxes, ha='left', va='top')

    # Add a box with n values and runtime values
    box_text = '\n'.join([f'n={n_values[i]}, runtime={format_runtime(runtimes[i])}' for i in range(len(n_values))])
    box_text += '\n' + '\n'.join(
        [f'n={predict_n_values[i]}, runtime={format_runtime(predicted_runtimes[i])}' for i in
         range(len(predict_n_values))])

    # Set the position of the box next to the x-axis title
    box_position = (0.677, 0.62)

    # Add the box with n values and runtime values
    plt.text(*box_position, box_text, transform=plt.gca().transAxes, ha='left', va='bottom',
             bbox=dict(facecolor='white', alpha=0.5))

    plt.show()


# Define the range of input sizes (n values)
n_values = [2, 3, 4]

# Lists to store the corresponding runtimes
runtimes = []

# Iterate over each input size
for n in n_values:
    # Measure the start time
    start_time = time.time()

    x = generate_subgraphs(n)
    print(len(x))

    # Measure the elapsed time
    elapsed_time = time.time() - start_time

    # Store the runtime
    runtimes.append(elapsed_time)

    # Create the corresponding txt file
    log_subgraphs(x, "subgraphs_{}.txt".format(n), n)

# Convert the lists to numpy arrays for curve fitting
n_values_arr = np.array(n_values)
runtimes_arr = np.array(runtimes)

# n values to predict runtime
predict_n_values = np.array([4, 5, 6])

plotData(n_values_arr, runtimes_arr, predict_n_values)

