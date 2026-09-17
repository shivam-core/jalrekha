import networkx as nx

def available_graph(network,closed):
    """Retain the fastest available parallel link with stable ID tie-breaking.

    Selection happens AFTER closures, so closing one parallel link can expose
    the next one. The original dataset remains an unsimplified directed multigraph.
    """
    graph=nx.DiGraph();graph.add_nodes_from(network['nodes'])
    for edge in sorted(network['edges'],key=lambda e:(e['travel_seconds'],e['id'])):
        if edge['id'] not in closed and not graph.has_edge(edge['u'],edge['v']):
            graph.add_edge(edge['u'],edge['v'],weight=edge['travel_seconds'],edge=edge)
    return graph
