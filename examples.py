import networkx as nx
import math
import random
from disjoint_path_functions import *
import os

figs_dir = './figs/'
os.makedirs(figs_dir, exist_ok=True)

#Small test example A
TestA_G = import_graph_from_file('./test_examples/TestA_edges.csv','./test_examples/TestA_nodes.csv')
path_edges = Bhandari_disjoint_paths(TestA_G,0,5,2)
path_pair = paths_from_edge_set(TestA_G,path_edges,0,5,2)
path_pair_length = path_len_sum(TestA_G,path_edges)
assert(LP_disjoint_paths(TestA_G,0,5,2)==path_pair_length)
print('TestA Minimum Edge-Disjoint Pair Path Length: '+str(path_pair_length))
path_viz(TestA_G,0,5,path_pair,figs_dir+'TestA.png')

#Small test example B
TestB_G = import_graph_from_file('./test_examples/TestB_edges.csv','./test_examples/TestB_nodes.csv')
path_edges = Bhandari_disjoint_paths(TestB_G,0,5,2)
path_pair = paths_from_edge_set(TestB_G,path_edges,0,5,2)
path_pair_length = path_len_sum(TestB_G,path_edges)
assert(LP_disjoint_paths(TestB_G,0,5,2)==path_pair_length)
print('TestB Minimum Edge-Disjoint Pair Path Length: '+str(path_pair_length))
path_viz(TestB_G,0,5,path_pair,figs_dir+'TestB.png')

#20x20 grid with random weights
grid20 = nx.grid_2d_graph(20,20).to_directed()
for e in grid20.edges():
    grid20.edges[e]['weight'] = random.random()
for v in grid20.nodes():
    grid20.nodes[v]['X'] = v[0]
    grid20.nodes[v]['Y'] = v[1]
path_edges = Bhandari_disjoint_paths(grid20,(1,1),(18,18),2)
path_pair = paths_from_edge_set(grid20,path_edges,(1,1),(18,18),2)
path_pair_length = path_len_sum(grid20,path_edges)
assert(math.isclose(LP_disjoint_paths(grid20,(1,1),(18,18),2),path_pair_length))
print('grid20 Minimum Edge-Disjoint Pair Path Length: '+str(path_pair_length))
path_viz(grid20,(1,1),(18,18),path_pair,figs_dir+'grid20.png')

#California road network
CA_G = import_graph_from_file('./road_networks/CA_edges.csv','./road_networks/CA_nodes.csv')
pared_CA_G = pare_graph(CA_G)
sacremento = find_nearest_node(pared_CA_G, -121.4944,38.5816)
san_diego = find_nearest_node(pared_CA_G, -117.1611,32.7157)
path_edges = Bhandari_disjoint_paths(CA_G,sacremento,san_diego,2)
path_pair = paths_from_edge_set(CA_G,path_edges,sacremento,san_diego,2)
path_pair_length = path_len_sum(CA_G,path_edges)
print('CA Minimum Edge-Disjoint Pair Path Length: '+str(path_pair_length))
path_viz(pared_CA_G.to_undirected(),sacremento,san_diego,path_pair,figs_dir+'CA_test.png', edge_width=.5,node_size = 0,path_width = 4)

#North America road network
NorthAm_G = import_graph_from_file('./road_networks/NorthAm_edges.csv','./road_networks/NorthAm_nodes.csv')
pared_NorthAm_G = pare_graph(NorthAm_G)
s,t = list(pared_NorthAm_G.nodes)[0],list(pared_NorthAm_G.nodes)[-1]
path_edges = Bhandari_disjoint_paths(NorthAm_G,s,t,2)
path_pair = paths_from_edge_set(NorthAm_G,path_edges,s,t,2)
path_pair_length = path_len_sum(NorthAm_G,path_edges)
print('NorthAm Minimum Edge-Disjoint Pair Path Length: '+str(path_pair_length))
path_viz(NorthAm_G.to_undirected(),s,t,path_pair,figs_dir+'NorthAm_test.png', edge_width=.5,node_size = 0,path_width = 4)


