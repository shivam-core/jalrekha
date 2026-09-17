from engine.roads import available_graph
from engine.routes import feasible_routes

def test_direction_parallel_closure_and_geometry():
    network={'nodes':{'a':[0,0],'b':[1,0],'c':[2,0]},'edges':[
        {'id':'ab','u':'a','v':'b','travel_seconds':1,'geometry':[[0,0],[.5,.1],[1,0]]},
        {'id':'ab2','u':'a','v':'b','travel_seconds':3,'geometry':[[0,0],[.5,-.1],[1,0]]},
        {'id':'bc','u':'b','v':'c','travel_seconds':1,'geometry':[[1,0],[2,0]]}]}
    o=[{'id':'o','node':'a','status':'usable','coordinates':[0,0]}];s=[{'id':'s','node':'c','usable':True}]
    g=available_graph(network,set());r=feasible_routes(g,o,s)['o','s'];assert r['edge_ids']==['ab','bc'];assert r['geometry']['coordinates']==[[0,0],[.5,.1],[1,0],[2,0]]
    g=available_graph(network,{'ab'});r=feasible_routes(g,o,s)['o','s'];assert r['edge_ids']==['ab2','bc']
    assert not feasible_routes(available_graph(network,{'bc'}),o,s)
    assert not feasible_routes(g,[dict(o[0],node='c')],[dict(s[0],node='a')])
    assert not feasible_routes(g,o,s,cutoff=1)
