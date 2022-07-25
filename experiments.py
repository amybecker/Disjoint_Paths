import networkx as nx
import random
from disjoint_path_functions import *
import time
import matplotlib.pyplot as plt
import os
import math


figs_dir = './figs/'
os.makedirs(figs_dir, exist_ok=True)


def time_single_run(graph, s, t, method):
    time0 = time.time()
    path_edges = Bhandari_disjoint_paths(graph,s, t,2, shortest_path_method=method)
    path_pair = paths_from_edge_set(graph,path_edges,s, t,2, shortest_path_method=method)
    time1 = time.time()
    return time1-time0,path_len_sum(graph,path_edges)

def run_compare_across_graph_size(graph, s, t, graph_name, n_reps, rand_weight = True, verbose = True):
    runtimes_dijkstra = []
    runtimes_bellmanford = []
    for rep in range(n_reps):
        if rand_weight:
            for e in graph.edges():
                graph.edges[e]['weight'] = random.random()
        time_dijkstra, cost_dijkstra = time_single_run(graph, s, t, Bhandari_dijkstra_mod)
        time_bellmanford, cost_bellmanford = time_single_run(graph, s, t, nx.bellman_ford_path)
        runtimes_dijkstra.append(time_dijkstra)
        runtimes_bellmanford.append(time_bellmanford)
        assert(math.isclose(cost_dijkstra,cost_bellmanford))
    if verbose:
        print(graph_name+' avg. runtime: '+str(sum(runtimes_dijkstra)/n_reps) + ' s (dijkstra), '+str(sum(runtimes_bellmanford)/n_reps) + ' s (bellmanford), ')
    return(runtimes_dijkstra,runtimes_bellmanford)

def plot_compare(runtime_dict_dijkstra, runtime_dict_bellmanford, figname,dpi = 300):
    fig,ax = plt.subplots()
    plt.plot([i for i in runtime_dict_dijkstra],[sum(runtime_dict_dijkstra[i])/len(runtime_dict_dijkstra[i]) for i in runtime_dict_dijkstra],zorder = 1, label = 'Dijkstra Mod')
    plt.scatter([i for i in runtime_dict_dijkstra],[sum(runtime_dict_dijkstra[i])/len(runtime_dict_dijkstra[i]) for i in runtime_dict_dijkstra],zorder = 1)
    plt.plot([i for i in runtime_dict_bellmanford],[sum(runtime_dict_bellmanford[i])/len(runtime_dict_bellmanford[i]) for i in runtime_dict_bellmanford],zorder = 1, label = 'Bellman-Ford')
    plt.scatter([i for i in runtime_dict_bellmanford],[sum(runtime_dict_bellmanford[i])/len(runtime_dict_bellmanford[i]) for i in runtime_dict_bellmanford],zorder = 1)
    plt.xlabel('|V|')
    plt.ylabel('average time (s)')
    plt.legend()
    plt.savefig(figname,dpi = dpi)


#compare average runtime for increasingly large nxn grids with random weights
runtime_dict_dijkstra = {}
runtime_dict_bellmanford = {}
for i in range(50,550,50):
    gridi = nx.grid_2d_graph(i,i).to_directed()
    runtime_dict_dijkstra[i**2], runtime_dict_bellmanford[i**2] = run_compare_across_graph_size(gridi, (1,1),(i-2,i-2), str(i) +'x'+str(i)+' grid', 10, rand_weight = True, verbose = True)

#plot graph size vs average runtime
plot_compare(runtime_dict_dijkstra, runtime_dict_bellmanford, figs_dir+'grid_runtime.png')

#compare average runtime for increasingly large erdos-renyi graphs
for p in [.15,.95]:
    runtime_dict_dijkstra = {}
    runtime_dict_bellmanford = {}
    for n in [i**2 for i in range(4,40,2)]:
        erdos_renyi_n = nx.erdos_renyi_graph(n,p = p, directed = True)
        runtime_dict_dijkstra[n], runtime_dict_bellmanford[n] = run_compare_across_graph_size(erdos_renyi_n,0,n-1, str(n) +'-node erdos-renyi (p='+str(p)+')', 10, rand_weight = True, verbose = True)
    plot_compare(runtime_dict_dijkstra, runtime_dict_bellmanford, figs_dir+'erdos_renyi_p'+str(p)+'_runtime.png')

