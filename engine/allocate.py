"""Identical feasibility for greedy and lexicographic max-flow/min-cost plans."""
import networkx as nx

def allocate(origins,shelters,routes,optimise=True):
    if optimise:
        flowgraph=nx.DiGraph();source=('source',);sink=('sink',);flowgraph.add_nodes_from([source,sink])
        for o in origins:flowgraph.add_edge(source,('o',o['id']),capacity=o['assumed_population'],weight=0)
        for s in shelters:flowgraph.add_edge(('s',s['id']),sink,capacity=s['capacity'] if s['usable'] else 0,weight=0)
        for (o,s),route in sorted(routes.items()):flowgraph.add_edge(('o',o),('s',s),capacity=sum(x['assumed_population'] for x in origins),weight=route['travel_seconds'])
        # NetworkX computes the maximum feasible amount, then minimum cost at that amount.
        flow=nx.max_flow_min_cost(flowgraph,source,sink)
        amounts={(o,s):flow.get(('o',o),{}).get(('s',s),0) for o,s in routes}
    else:
        remaining={s['id']:s['capacity'] if s['usable'] else 0 for s in shelters};amounts={}
        for o in sorted(origins,key=lambda x:x['id']):
            left=o['assumed_population']
            choices=sorted(((r['travel_seconds'],s) for (oid,s),r in routes.items() if oid==o['id']))
            for _,sid in choices:
                take=min(left,remaining[sid]);amounts[o['id'],sid]=take;remaining[sid]-=take;left-=take
    allocations=[{'origin_id':o,'shelter_id':s,'people':n,**routes[o,s],'explanation':'Chosen by the capacity-constrained plan; route and receiving capacity are feasible.' if optimise else 'Assigned in origin-ID order to the nearest reachable candidate with remaining capacity.'} for (o,s),n in sorted(amounts.items()) if n>0]
    origin_rows=[]
    for o in origins:
        allocated=sum(a['people'] for a in allocations if a['origin_id']==o['id']);unmet=o['assumed_population']-allocated
        category='unknown_or_unavailable_origin' if o['status']!='usable' else 'isolated' if not any(oid==o['id'] for oid,_ in routes) else 'capacity_unserved'
        origin_rows.append({**o,'allocated':allocated,'unmet':unmet,'unmet_category':category if unmet else None})
    total={'population':sum(o['assumed_population'] for o in origins),'allocated':sum(a['people'] for a in allocations),'isolated':0,'capacity_unserved':0,'unknown_or_unavailable_origin':0,'person_seconds':sum(a['people']*a['travel_seconds'] for a in allocations)}
    for o in origin_rows:
        if o['unmet_category']:total[o['unmet_category']]+=o['unmet']
    total['unallocated']=total['population']-total['allocated'];total['mean_travel_seconds']=total['person_seconds']/total['allocated'] if total['allocated'] else None
    shelter_rows=[]
    for s in shelters:
        n=sum(a['people'] for a in allocations if a['shelter_id']==s['id']);shelter_rows.append({**s,'allocated':n,'remaining':(s['capacity'] if s['usable'] else 0)-n})
    total['usable_capacity']=sum(s['capacity'] for s in shelters if s['usable'])
    return {'allocations':allocations,'origins':origin_rows,'shelters':shelter_rows,'totals':total}
