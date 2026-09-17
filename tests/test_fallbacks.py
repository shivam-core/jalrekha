import json
from engine.load import ROOT
from engine.scenario import compute
from engine.schemas import ScenarioInput

def test_saved_results_match_engine():
    index=json.loads((ROOT/'public/data/scenarios/index.json').read_text())
    for entry in index:
        saved=json.loads((ROOT/'public'/entry['url'].lstrip('/')).read_text())
        assert saved==compute(ScenarioInput.model_validate(entry['input']))
