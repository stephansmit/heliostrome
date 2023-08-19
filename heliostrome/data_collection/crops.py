from typing import List, Optional
from aquacrop.entities.crops.crop_params import crop_params
from pydantic import BaseModel, Field


class HeliostromeCrop(BaseModel):
    Name: str
    Aer: Optional[float] = None
    LagAer: Optional[float] = None
    CCx: float = Field(
        description="maximum canopy cover for that plant density under optimal conditions [m2/m2]"
    )
    CDC: float = Field(description="canopy decline coefficient")
    CDC_CD: Optional[float] = None
    CGC: float = Field(description="canopy growth coefficient")
    CGC_CD: Optional[float] = None
    CalendarType: int
    CropType: int
    Determinant: float
    ETadj: Optional[float] = None
    Emergence: float
    EmergenceCD: Optional[float] = None
    Flowering: float
    FloweringCD: Optional[float] = None
    GDD_lo: int
    GDD_up: float
    GDDmethod: int = Field(description="growing degree day method")
    HI0: float = Field(description="reference harvest index [%]")
    HIstart: float
    HIstartCD: Optional[float] = None
    Kcb: float
    LagAer: Optional[float] = None
    Maturity: float
    MaturityCD: Optional[float] = None
    MaxRooting: float
    MaxRootingCD: Optional[float] = None
    PlantMethod: float
    PlantPop: float
    PolColdStress: int = Field(description="pollination cold stress coefficient")
    PolHeatStress: int = Field(description="pollination heat stress coefficient")
    SeedSize: float
    Senescence: float
    SenescenceCD: Optional[float] = None
    SwitchGDD: int
    SxBotQ: float = Field(
        description="bottom root extraction rate [m3/m3/day] (page 108)"
    )
    SxTopQ: float = Field(description="top root extraction rate [m3/m3/day] (page 108)")
    Tbase: float = Field(
        description="base temperature (below which crop development does not progress) [degC] (page 21)"
    )
    Tmax_lo: float
    Tmax_up: float
    Tmin_lo: float
    Tmin_up: float
    TrColdStress: int = Field(description="transpiration cold stress coefficient")
    Tupp: float = Field(
        description="upper temperature (above which crop development no longer increases with an increase in air temperature) [degC] (page 21)"
    )
    WP: float = Field(description="water productivity")
    WPy: float
    YldForm: float
    YldFormCD: Optional[float] = None
    Zmax: float
    Zmin: float
    a_HI: float = Field(
        description="harvest index crop parameter a (page 145)", ge=0.5, le=40
    )
    b_HI: float = Field(
        description="harvest index crop parameter b (page 147)", ge=1, le=20
    )
    dHI0: float
    dHI_pre: float
    exc: float = Field(description="excess coefficient (page 142)")
    fage: float = Field(description="age factor (page 95)")
    fshape_r: float
    fshape_w1: float
    fshape_w2: float
    fshape_w3: float
    fshape_w4: int
    fsink: float
    p_lo1: float
    p_lo2: int
    p_lo3: int
    p_lo4: int
    p_up1: float
    p_up2: float
    p_up3: float
    p_up4: float


def _get_aquacrop_names():
    return list(crop_params.keys())


def get_all_crop_data() -> List[HeliostromeCrop]:
    return [
        HeliostromeCrop(**crop_params[crop_name]) for crop_name in _get_aquacrop_names()
    ]


def get_crop_data(crop_name: str) -> HeliostromeCrop:
    return HeliostromeCrop(**crop_params[crop_name])
