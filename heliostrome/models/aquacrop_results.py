from datetime import datetime
from pydantic import BaseModel, Field


class CropGrowth(BaseModel):
    time: datetime
    time_step_counter: int
    season_counter: int
    dap: int = Field(description="days after planting [day]")
    gdd: float = Field(description="growing degree days [degCday]")
    gdd_cum: float = Field(description="cumulative growing degree days [degCday]")
    z_root: float = Field(description="root zone depth [m]")
    canopy_cover: float = Field(description="canopy cover [m2/m2]", ge=0, le=1)
    canopy_cover_ns: float = Field(
        description="canopy cover no stress [m2/m2]", ge=0, le=1
    )
    biomass: float = Field(description="biomass [Mg/ha]")
    biomass_ns: float = Field(description="biomass no stress [Mg/ha]")
    harvest_index: float = Field(description="harvest index [%]")
    harvest_index_adj: float = Field(description="adjusted harvest index [%]")
    yield_: float


class SimulationResult(BaseModel):
    season: int = Field(alias="Season")
    crop_type: str = Field(alias="crop Type")
    harvest_date_step: int = Field(alias="Harvest Date (Step)")
    yield_tonneha: float = Field(alias="Yield (tonne/ha)")
    seasonal_irrigation_mm: float = Field(alias="Seasonal irrigation (mm)")
    harvest_date: datetime = Field(alias="Harvest Date (YYYY/MM/DD)")


class WaterFlux(BaseModel):
    time: datetime
    time_step_counter: float
    season_counter: float
    dap: float = Field(description="days after planting [day]")
    Wr: float = Field(description="water content root zone [m3/m3]")
    z_gw: float = Field(description="ground water depth [m]")
    surface_storage: float
    IrrDay: float = Field(description="irrigation on current day")
    Infl: float = Field(description="infiltration so far")
    Runoff: float = Field(description="surface runoff [mm/day]")
    DeepPerc: float = Field(description="deep percolation [mm/day]")
    CR: float = Field(description="capillary rise [mm/day]")
    GwIn: float = Field(description="ground water inflow")
    Es: float = Field(description="surface evaporation current day [mm/day]")
    EsPot: float = Field(
        description="Potential surface evaporation current day [mm/day]"
    )
    Tr: float = Field(description="daily crop transpiration [mm/day]")
    TrPot: float = Field(description="daily potential crop transpiration [mm/day]")


class WaterStorage(BaseModel):
    time: datetime
    time_step_counter: float
    growing_season: float
    dap: float = Field(description="days after planting")
    th1: float = Field(description="water content of soil compartment 1 [m3/m3]")
    th2: float = Field(description="water content of soil compartment 2 [m3/m3]")
    th3: float = Field(description="water content of soil compartment 3 [m3/m3]")
    th4: float = Field(description="water content of soil compartment 4 [m3/m3]")
    th5: float = Field(description="water content of soil compartment 5 [m3/m3]")
    th6: float = Field(description="water content of soil compartment 6 [m3/m3]")
    th7: float = Field(description="water content of soil compartment 7 [m3/m3]")
    th8: float = Field(description="water content of soil compartment 8 [m3/m3]")
    th9: float = Field(description="water content of soil compartment 9 [m3/m3]")
    th10: float = Field(description="water content of soil compartment 10 [m3/m3]")
    th11: float = Field(description="water content of soil compartment 11 [m3/m3]")
    th12: float = Field(description="water content of soil compartment 12 [m3/m3]")
