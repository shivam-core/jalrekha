import hashlib,json
from .load import load_data
from .roads import available_graph
from .routes import feasible_routes
from .allocate import allocate
from .schemas import ScenarioInput

def compute(request:ScenarioInput,data=None):
    data=data or load_data();network=data['network'];locations=data['locations'];manifest=data['manifest']
    edge_ids={e['id'] for e in network['edges']};shelter_ids={s['id'] for s in locations['shelters']}
    if set(request.closed_edge_ids)-edge_ids:raise ValueError('Unknown road link ID')
    if set(request.shelter_overrides)-shelter_ids:raise ValueError('Unknown candidate shelter ID')
    applied=request.canonical();hazard=data['hazards']['levels'][str(round(request.level_m*10))]
    blocked=set(hazard['unavailable_edge_ids'])|set(hazard['unknown_edge_ids'])|set(request.closed_edge_ids)
    origins=[dict(o,status=hazard['origin_status'][o['id']]) for o in locations['origins']]
    shelters=[]
    for s in locations['shelters']:
        override=applied['shelter_overrides'].get(s['id'],{});opened=override.get('open',s['default_open']);status=hazard['shelter_status'][s['id']]
        shelters.append({**s,'open':opened,'status':status,'usable':opened and status=='usable','capacity':override.get('capacity',s['capacity'])})
    if sum(s['capacity'] for s in shelters)>50000:raise ValueError('Aggregate assumed capacity must not exceed 50,000')
    graph=available_graph(network,blocked);routes=feasible_routes(graph,origins,shelters,manifest['settings']['travel_cutoff_seconds'])
    optimal=allocate(origins,shelters,routes);baseline=allocate(origins,shelters,routes,False)
    delta=optimal['totals']['allocated']-baseline['totals']['allocated'];costdelta=baseline['totals']['person_seconds']-optimal['totals']['person_seconds']
    sid=hashlib.sha256((manifest['dataset_version']+json.dumps(applied,sort_keys=True,separators=(',',':'))).encode()).hexdigest()[:20]
    return {'schema_version':'1','dataset_version':manifest['dataset_version'],'scenario_id':sid,'input':applied,'hazard':dict(hazard,manually_closed_edge_ids=request.closed_edge_ids,total_unavailable_directed_links=len(blocked)),**optimal,'baseline':baseline,'comparison':{'additional_allocated':delta,'person_seconds_saved_at_equal_allocation':costdelta if delta==0 else None,'interpretation':f'{delta} additional people allocated. Total travel cost is not comparable when allocated totals differ.' if delta else ('Same number allocated; optimiser reduces total person-seconds.' if costdelta>0 else 'Both plans allocate the same number with equal total travel cost.')},'assumptions':manifest['assumptions']}
