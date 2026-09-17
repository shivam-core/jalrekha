import itertools
from engine.allocate import allocate

def fixture():
    origins=[{'id':f'o{i}','assumed_population':2,'status':'usable'} for i in (1,2)]
    shelters=[{'id':f's{i}','capacity':2,'usable':True} for i in (1,2)]
    routes={('o1','s1'):{'travel_seconds':1},('o1','s2'):{'travel_seconds':2},('o2','s1'):{'travel_seconds':1}}
    return origins,shelters,routes

def test_known_optimum_by_enumeration():
    o,s,r=fixture();result=allocate(o,s,r);baseline=allocate(o,s,r,False)
    feasible=[]
    for a,b,c in itertools.product(range(3),repeat=3):
        if a+b<=2 and a+c<=2 and b<=2 and c<=2:feasible.append((a+b+c,a+2*b+c))
    best=min(feasible,key=lambda v:(-v[0],v[1]))
    assert (result['totals']['allocated'],result['totals']['person_seconds'])==best==(4,6)
    assert baseline['totals']['allocated']==2

def test_capacity_monotonicity_and_zero():
    o,s,r=fixture();previous=0
    for cap in range(5):
        s[1]['capacity']=cap;out=allocate(o,s,r);assert out['totals']['allocated']>=previous;previous=out['totals']['allocated']
        assert all(x['allocated']<=x['capacity'] for x in out['shelters'])

def test_unusable_and_bookkeeping():
    o,s,r=fixture();o[0]['status']='unknown';r={k:v for k,v in r.items() if k[0]!='o1'};s[0]['usable']=False;r={k:v for k,v in r.items() if k[1]!='s1'}
    out=allocate(o,s,r);t=out['totals'];assert t['allocated']==0;assert t['isolated']==2;assert t['unknown_or_unavailable_origin']==2
    assert t['population']==sum(t[k] for k in ['allocated','isolated','capacity_unserved','unknown_or_unavailable_origin'])
