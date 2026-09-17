"""Read-only prepared data. No geographic downloads or native imports at runtime."""
from pathlib import Path
from functools import lru_cache
import json
ROOT=Path(__file__).resolve().parents[1]
@lru_cache(maxsize=1)
def load_data():
    return {name:json.loads((ROOT/'data/processed'/f'{name}.json').read_text()) for name in ('network','locations','hazards','manifest')}
