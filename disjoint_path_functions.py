import networkx as nx
import matplotlib.pyplot as plt
import csv
import numpy as np
from pulp import *
from networkx.algorithms.connectivity.edge_kcomponents import bridge_components


#implementation of Bhandari 1999 edge-disjoint path pair
def Bhandari_disjoint_paths(graph,s,t,k):
    p0 = nx.bellman_ford_path(graph,s,t)
    p0_edges = {(p0[i],p0[i+1]) for i in range(len(p0)-1)}
    for i in range(k-1):
        graph_alt = graph.copy()
        for e in p0_edges:
            graph_alt.remove_edge(e[0],e[1])
            graph_alt.add_edge(e[1],e[0])
            graph_alt.edges[(e[1],e[0])]['weight'] = -1*graph.edges[e]['weight']
        pi = nx.bellman_ford_path(graph_alt,s,t)
        pi_edges = {(pi[i],pi[i+1]) for i in range(len(pi)-1)}
        dup_edges = {e for e in pi_edges if (e[1],e[0]) in p0_edges}
        p0_edges = p0_edges.union(pi_edges) -  dup_edges - {(e[1],e[0]) for e in dup_edges}
    return p0_edges

#finds path solutions from set of solution's edges
def paths_from_edge_set(graph, edge_set,s,t,k):
    subgraph = nx.edge_subgraph(graph,edge_set).copy()
    out_paths = []
    for i in range(k):
        pi = nx.bellman_ford_path(subgraph,s,t)
        out_paths.append(pi)
        subgraph.remove_edges_from([(pi[i],pi[i+1]) for i in range(len(pi)-1)])
    return out_paths

#solution cost
def path_len_sum(graph,edge_set):
    return sum([graph.edges[e]["weight"] for e in edge_set])

#LP solver for disjoint paths
def LP_disjoint_paths(graph,s,t,k):
    problem = LpProblem('k_disjoint_paths', LpMinimize)
    #decision variables
    var_dict = {}
    for e in graph.edges():
        var_dict[e] = LpVariable('var_'+str(e).replace(' ',''), lowBound=0 , cat=LpBinary)
    #objective function
    problem += sum([graph.edges[e]['weight']*var_dict[e] for e in graph.edges()])
    #constraints
    problem += sum([var_dict[e] for e in graph.out_edges(s)]) == k
    problem += sum([var_dict[e] for e in graph.in_edges(s)]) == 0
    problem += sum([var_dict[e] for e in graph.in_edges(t)]) == k
    problem += sum([var_dict[e] for e in graph.out_edges(t)]) == 0
    for v in graph.nodes():
        if v not in [s,t]:
            problem += sum([var_dict[e] for e in graph.out_edges(v)])- sum([var_dict[e] for e in graph.in_edges(v)]) == 0
    problem.solve(GLPK_CMD(msg=0))
    return value(problem.objective)

#read in graph from edge and node files
def import_graph_from_file(edge_len_file, node_loc_file = None, directed = False):
    G = nx.DiGraph()
    with open(edge_len_file, mode='r', encoding='utf-8-sig') as edge_csv_file:
        edge_csv_reader = csv.reader(edge_csv_file)
        for row in edge_csv_reader:
            G.add_edge(int(row[0]),int(row[1]))
            G.edges[(int(row[0]),int(row[1]))]['weight'] = float(row[2])
            if not directed:
                G.add_edge(int(row[1]),int(row[0]))
                G.edges[(int(row[1]),int(row[0]))]['weight'] = float(row[2])
    if node_loc_file:
        with open(node_loc_file, mode='r', encoding='utf-8-sig') as node_csv_file:
            node_csv_reader = csv.reader(node_csv_file)
            for row in node_csv_reader:
                G.nodes[int(row[0])]['X'] = float(row[1])
                G.nodes[int(row[0])]['Y'] = float(row[2])
    return G

#pare input graph to 2-edge connected component
def pare_graph(graph):
    out_graph = graph.to_undirected()
    bridge_comps = list(bridge_components(out_graph))
    max_comp_size = max([len(comp) for comp in bridge_comps])
    for c in bridge_comps:
        if len(c) == max_comp_size:
            return nx.subgraph(graph,c)

#find node in graph closest to input point
def find_nearest_node(graph,pt_X,pt_Y):
    nodelist = list(graph.nodes())
    node_x_vals = np.array([graph.nodes[nodelist[i]]["X"] for i in range(len(nodelist))])
    node_y_vals = np.array([graph.nodes[nodelist[i]]["Y"] for i in range(len(nodelist))])
    dist = np.sqrt((pt_X-node_x_vals)**2+(pt_Y-node_y_vals)**2)
    return nodelist[np.argmin(dist)]

#visualize graph with solution paths highlighted
def path_viz(graph,s,t,path_list,fig_name, edge_width = 2,node_size = 10,dpi = 300, path_arrows = False, path_width = 6):
    fig,ax = plt.subplots()
    pos = {v:(graph.nodes[v]['X'],graph.nodes[v]['Y']) for v in graph.nodes()}
    nx.draw(graph, pos=pos, node_size = node_size,node_color = 'black',arrowstyle = '-', width = edge_width)
    nx.draw_networkx_nodes(graph, pos=pos, nodelist = [s,t], node_size = 200,node_color = 'lightgray', edgecolors = 'black')
    nx.draw_networkx_labels(graph, pos = pos, labels={s:'A',t:'Z'})
    path_colors = ['tab:green','tab:purple','tab:blue','tab:orange','tab:gray','tab:pink','tab:olice']
    for i in range(len(path_list)):
        edge_pathi = [(path_list[i][j],path_list[i][j+1]) for j in range(len(path_list[i])-1)]
        nx.draw_networkx_edges(graph, pos=pos, arrows = path_arrows, edgelist = edge_pathi, node_size = 0, width = path_width,edge_color = path_colors[i%len(path_colors)])
    plt.tight_layout()
    plt.savefig(fig_name,dpi = dpi)
    plt.close('all')
