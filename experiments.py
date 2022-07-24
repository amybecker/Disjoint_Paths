import networkx as nx
import random
from disjoint_path_functions import *
import time
import matplotlib.pyplot as plt
import os

figs_dir = './figs/'
os.makedirs(figs_dir, exist_ok=True)

#find average runtime for increasingly large nxn grids with random weights
n_reps = 10
runtime_dict = {}
for i in range(50,550,50):
    runtimes_i = []
    gridi = nx.grid_2d_graph(i,i).to_directed()
    for rep in range(n_reps):
        for e in gridi.edges():
            gridi.edges[e]['weight'] = random.random()
        for v in gridi.nodes():
            gridi.nodes[v]['X'] = v[0]
            gridi.nodes[v]['Y'] = v[1]
        time0 = time.time()
        path_edges = Bhandari_disjoint_paths(gridi,(1,1),(i-2,i-2),2)
        path_pair = paths_from_edge_set(gridi,path_edges,(1,1),(i-2,i-2),2)
        time1 = time.time()
        runtimes_i.append(time1-time0)
    runtime_dict[i] = runtimes_i
    print(str(i)+' x '+str(i)+' grid avg. runtime: '+str(sum(runtime_dict[i])/n_reps) + ' s')

#plot graph size vs average runtime
fig,ax = plt.subplots()
plt.plot([i**2 for i in runtime_dict],[sum(runtime_dict[i])/len(runtime_dict[i]) for i in runtime_dict],zorder = 1)
plt.scatter([i**2 for i in runtime_dict],[sum(runtime_dict[i])/len(runtime_dict[i]) for i in runtime_dict],zorder = 1)
plt.xlabel('|V|')
plt.ylabel('average time (s)')
plt.savefig(figs_dir+'runtime.png',dpi = 300)
    