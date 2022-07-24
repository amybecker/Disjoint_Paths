# Disjoint_Paths
Implementation of Bhandari's disjoint-path algorithm.

Based on Bhandari's algorithm published in: Bhandari, Ramesh. Survivable networks: algorithms for diverse routing. Springer Science & Business Media, 1999.([link](https://link.springer.com/book/9780792383819))

We test the implementation using toy examples as well as grids with random edge costs and road networks.  The road networks for North American and California are datasets from research done at the University of Utah and can be found [here](https://www.cs.utah.edu/~lifeifei/SpatialDataset.htm). 

Users can test their own graph examples using an edge input csv file with one row for each edge in the form [u,v,cost(u,v)] and a node input csv file with one row for each node in the form [v, x_coord(v), y_coord(v)].  The node input file is only required for visualization methods.  Users can alternatively directly define their graphs using networkx graph-generating functionalitiy.

We include a PuLP linear programming solver for the problem in order to test and verify solutions, but the LP is too slow to run the large instances on.

Finally, we include a basic visualization method to map the graph and solution paths.

