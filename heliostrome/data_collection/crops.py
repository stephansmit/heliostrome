from typing import List, Optional
from aquacrop.entities.crops.crop_params import crop_params
from pydantic import BaseModel


class HeliostromeCrop(BaseModel):
    Name: str
    Aer: Optional[float] = None
    LagAer: Optional[float] = None
    CCx: float
    CDC: float
    CDC_CD: Optional[float] = None
    CGC: float
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
    GDDmethod: int
    HI0: float
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
    PolColdStress: int
    PolHeatStress: int
    SeedSize: float
    Senescence: float
    SenescenceCD: Optional[float] = None
    SwitchGDD: int
    SxBotQ: float
    SxTopQ: float
    Tbase: float
    Tmax_lo: float
    Tmax_up: float
    Tmin_lo: float
    Tmin_up: float
    TrColdStress: int
    Tupp: float
    WP: float
    WPy: float
    YldForm: float
    YldFormCD: Optional[float] = None
    Zmax: float
    Zmin: float
    a_HI: float
    b_HI: float
    dHI0: float
    dHI_pre: float
    exc: float
    fage: float
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
