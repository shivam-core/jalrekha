"""Slim, stateless Vercel entrypoint; all GIS is prepared locally."""
import json
from fastapi import FastAPI,HTTPException,Request
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from engine.schemas import ScenarioInput
from engine.load import load_data
from engine.scenario import compute
app=FastAPI(title='JALREKHA',version='1.0.0')
@app.get('/')
def index():return RedirectResponse('/index.html')
@app.get('/api/health')
def health():return {'status':'ok','schema_version':'1','dataset_version':load_data()['manifest']['dataset_version'],'mode':'HAND scenario planning'}
@app.get('/api/meta')
def meta():
    data=load_data();return {**data['manifest'],**data['locations'],'limits':{'max_capacity_per_shelter':10000,'max_aggregate_capacity':50000,'max_request_bytes':32768},'default_input':ScenarioInput().canonical()}
def run(value):
    try:return compute(value)
    except ValueError as exc:raise HTTPException(422,str(exc)) from exc
@app.get('/api/scenario')
def get_scenario(h:float=0.0):
    try:value=ScenarioInput(level_m=h)
    except ValidationError:raise HTTPException(422,'Choose a finite level from 0 to 8 m in 0.5 m steps')
    return run(value)
@app.post('/api/scenario')
async def post_scenario(request:Request):
    body=bytearray()
    async for chunk in request.stream():
        body.extend(chunk)
        if len(body)>32768:raise HTTPException(413,'Scenario request exceeds 32 KiB')
    try:value=ScenarioInput.model_validate_json(bytes(body))
    except ValidationError as exc:
        raise HTTPException(422,[{'loc':list(e['loc']),'message':e['msg']} for e in exc.errors()]) from exc
    return run(value)
