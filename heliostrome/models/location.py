from pydantic import BaseModel, Field, computed_field
from typing import Optional
from pvlib.location import lookup_altitude


class Location(BaseModel):
    longitude: float = Field(ge=-179.975, le=179.975)
    latitude: float = Field(ge=-49.975, le=49.975)

    @computed_field
    @property
    def altitude_m(self) -> float:
        return lookup_altitude(self.latitude, self.longitude)
