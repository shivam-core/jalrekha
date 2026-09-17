import networkx as nx

def feasible_routes(graph,origins,shelters,cutoff=2700):
    result={}
    for origin in origins:
        if origin['status']!='usable':continue
        lengths,paths=nx.single_source_dijkstra(graph,origin['node'],cutoff=cutoff,weight='weight')
        for shelter in shelters:
            if not shelter['usable'] or shelter['node'] not in paths:continue
            nodes=paths[shelter['node']];edges=[graph[u][v]['edge'] for u,v in zip(nodes,nodes[1:])]
            coords=[]
            for edge in edges:coords.extend(edge['geometry'] if not coords else edge['geometry'][1:])
            if not coords:coords=[origin['coordinates'],origin['coordinates']]
            result[(origin['id'],shelter['id'])]={'travel_seconds':int(lengths[shelter['node']]),'edge_ids':[e['id'] for e in edges],'geometry':{'type':'LineString','coordinates':coords}}
    return result
