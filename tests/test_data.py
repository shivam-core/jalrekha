import pytest
from engine.load import load_data
from engine.scenario import compute
from engine.schemas import ScenarioInput

@pytest.mark.parametrize('level',[x/2 for x in range(17)])
def test_real_scenario_invariants(level):
    data=load_data();r=compute(ScenarioInput(level_m=level));t=r['totals'];b=r['baseline']['totals']
    assert t['population']==sum(t[k] for k in ['allocated','isolated','capacity_unserved','unknown_or_unavailable_origin'])
    assert t['allocated']>=b['allocated']
    if t['allocated']==b['allocated']:assert t['person_seconds']<=b['person_seconds']
    assert all(s['allocated']<=s['capacity'] and (s['usable'] or s['allocated']==0) for s in r['shelters'])
    edges={e['id']:e for e in data['network']['edges']};blocked=set(r['hazard']['unavailable_edge_ids'])|set(r['hazard']['unknown_edge_ids'])
    for a in r['allocations']+r['baseline']['allocations']:
        assert not blocked.intersection(a['edge_ids'])
        path=[edges[e] for e in a['edge_ids']]
        assert all(e['v']==f['u'] for e,f in zip(path,path[1:]))
        origin=next(o for o in r['origins'] if o['id']==a['origin_id']);shelter=next(s for s in r['shelters'] if s['id']==a['shelter_id'])
        assert a['geometry']['coordinates'][0]==origin['coordinates'];assert a['geometry']['coordinates'][-1]==shelter['coordinates']
        assert a['travel_seconds']==sum(e['travel_seconds'] for e in path)

def test_closure_changes_path():
    request=ScenarioInput(level_m=0);r=compute(request);edge=r['allocations'][0]['edge_ids'][0]
    changed=compute(ScenarioInput(level_m=0,closed_edge_ids=[edge]))
    assert all(edge not in a['edge_ids'] for a in changed['allocations']+changed['baseline']['allocations'])
    assert r['allocations']!=changed['allocations']

def test_real_coordinates_weights_and_nodes():
    d=load_data();n=d['network'];assert len(n['nodes'])>1000
    assert len({e['id'] for e in n['edges']})==len(n['edges'])
    assert all(73<c[0]<75 and 18<c[1]<20 for c in n['nodes'].values())
    assert all(e['travel_seconds']>0 and e['geometry'][0]==n['nodes'][e['u']] and e['geometry'][-1]==n['nodes'][e['v']] for e in n['edges'])
    assert all(x['node'] in n['nodes'] for x in d['locations']['origins']+d['locations']['shelters'])
