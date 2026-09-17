import pytest
from fastapi.testclient import TestClient
from app import app
client=TestClient(app)

def test_health_meta_and_default():
    assert client.get('/api/health').json()['status']=='ok'
    assert len(client.get('/api/meta').json()['origins'])==6
    assert client.get('/api/scenario').status_code==200

@pytest.mark.parametrize('payload',[{'level_m':-1},{'level_m':.2},{'level_m':9},{'level_m':'2.5'},{'level_m':True},{'level_m':float('nan')},{'level_m':float('inf')},{'closed_edge_ids':['bogus']},{'shelter_overrides':{'bogus':{'open':True}}},{'shelter_overrides':{'shelter-1':{'capacity':-1}}},{'shelter_overrides':{'shelter-1':{'capacity':10001}}},{'shelter_overrides':{'shelter-1':{'capacity':1.2}}},{'shelter_overrides':{'shelter-1':{'open':'true'}}},{'extra':1}])
def test_bad_inputs(payload):
    import json
    assert client.post('/api/scenario',content=json.dumps(payload)).status_code==422

@pytest.mark.parametrize('h',['NaN','inf','-inf','0.3','9'])
def test_bad_get(h):assert client.get('/api/scenario',params={'h':h}).status_code==422

def test_size_and_malformed():
    assert client.post('/api/scenario',content='x'*32769).status_code==413
    assert client.post('/api/scenario',content='{').status_code==422

def test_no_mutation():
    before=client.get('/api/scenario').json();client.post('/api/scenario',json={'shelter_overrides':{'shelter-1':{'capacity':0}}});assert client.get('/api/scenario').json()==before
