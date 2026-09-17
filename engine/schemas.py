"""Version 1 request contract. IDs are strings; time is integer seconds."""
import math
from pydantic import BaseModel, ConfigDict, Field, field_validator
class ShelterOverride(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    open: bool | None = None
    capacity: int | None = Field(default=None,ge=0,le=10000)
class ScenarioInput(BaseModel):
    model_config=ConfigDict(extra='forbid')
    level_m: float = 0.0
    closed_edge_ids: list[str] = Field(default_factory=list,max_length=10000)
    shelter_overrides: dict[str,ShelterOverride] = Field(default_factory=dict,max_length=10)
    @field_validator('level_m',mode='before')
    @classmethod
    def level(cls,v):
        if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or not 0<=v<=8 or v*10 not in range(0,81,5):
            raise ValueError('Choose a supported HAND level from 0 to 8 m in 0.5 m steps')
        return float(v)
    @field_validator('closed_edge_ids')
    @classmethod
    def unique_ids(cls,v):return sorted(set(v))
    def canonical(self):
        return {'level_m':self.level_m,'closed_edge_ids':self.closed_edge_ids,'shelter_overrides':{k:v.model_dump(exclude_none=True) for k,v in sorted(self.shelter_overrides.items())}}
