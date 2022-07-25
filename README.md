# Disjoint_Paths
Implementation of Bhandari's disjoint-path algorithm as published in: 

- Bhandari, Ramesh. [Survivable networks: algorithms for diverse routing.](https://link.springer.com/book/9780792383819) Springer Science & Business Media, 1999.

We test the implementation using toy examples as well as grids with random edge costs and road networks.  The road networks for North American and California are datasets from research done at the University of Utah and can be found [here](https://www.cs.utah.edu/~lifeifei/SpatialDataset.htm). 

Users can test their own graph examples using an edge input csv file with one row for each edge in the form [u,v,cost(u,v)] and a node input csv file with one row for each node in the form [v, x_coord(v), y_coord(v)].  The node input file is only required for visualization methods.  Users can alternatively directly define their graphs using networkx graph-generating functionalitiy.

We include a PuLP linear programming solver for the problem in order to test and verify solutions, but the LP is too slow to run the large instances on.

We also include a basic visualization method to map the graph and solution paths.

All functions are in the disjoint_path_functions.py file.

Users can run the examples.py file to solve and produce maps for our testing examples.

Finally, experiments.py compares shortest-path methods (Bhandari's modified Dijkstra vs Bellman-Ford) for many repetitions on grid graphs and Erdős-Rényi random graphs of increasing size with random edge costs and then plots the relationship between graph size and runtime for these runs.

