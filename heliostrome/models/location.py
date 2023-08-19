from pydantic import BaseModel, Field
from typing import Optional


class Location(BaseModel):
    longitude: float = Field(ge=-179.975, le=179.975)
    latitude: float = Field(ge=-49.975, le=49.975)
    altitude: Optional[float] = None
