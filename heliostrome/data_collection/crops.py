from typing import List, Optional
from aquacrop.entities.crops.crop_params import crop_params
from pydantic import BaseModel, Field


class HeliostromeCrop(BaseModel):
    Name: str
    Aer: Optional[float] = Field(
        default=None,
        description="Vol (%) below saturation at which stress begins to occur due to deficient aeration",
    )
    LagAer: Optional[float] = Field(
        default=None,
        description="number of days lag before aeration stress affects crop growth",
    )
    CCx: float = Field(description="maximum canopy cover (fraction of soil cover)")
    CDC: float = Field(description="canopy decline coefficient (fraction per gdd)")
    CDC_CD: Optional[float] = Field(
        default=None, description="canopy decline coefficient (fraction per gdd)"
    )
    CGC: float = Field(description="canopy growth coefficient (fraction per gdd)")
    CGC_CD: Optional[float] = Field(
        default=None, description="canopy growth coefficient (fraction per gdd)"
    )
    CalendarType: int = Field(
        description="calendar Type (1 = Calendar days, 2 = Growing degree days)"
    )
    CropType: int = Field(
        description="crop Type (1 = Leafy vegetable, 2 = Root/tuber, 3 = Fruit/grain)"
    )
    Determinant: float = Field(
        description="crop Determinancy (0 = Indeterminant, 1 = Determinant)"
    )
    ETadj: Optional[float] = Field(
        default=None,
        description="Adjustment to water stress thresholds depending on daily ET0 (0 = No, 1 = Yes)",
    )
    Emergence: float = Field(
        description="growing degree/calendar days from sowing to emergence/transplant"
    )
    EmergenceCD: Optional[float] = None
    Flowering: float = Field(
        description="duration of flowering in growing degree/calendar days (-999 for non-fruit/grain crops)"
    )
    FloweringCD: Optional[float] = None
    GDD_lo: int = Field(
        description="Growing degree days (degC/day) at which no crop transpiration occurs"
    )
    GDD_up: float = Field(
        description="minimum growing degree days (degC/day) required for full crop transpiration potential"
    )
    GDDmethod: int = Field(description="growing degree day method")
    HI0: float = Field(description="reference harvest index [%]")
    HIstart: float = Field(
        description="growing degree/calendar days from sowing to start of yield_ formation"
    )
    HIstartCD: Optional[float] = None
    Kcb: float = Field(
        description="Crop coefficient when canopy growth is complete but prior to senescence"
    )
    LagAer: Optional[float] = None
    Maturity: float = Field(
        description="Growing degree/Calendar days from sowing to maturity"
    )
    MaturityCD: Optional[float] = None
    MaxRooting: float
    MaxRootingCD: Optional[float] = None
    PlantMethod: float = Field(
        description="planting method (0 = Transplanted, 1 =  Sown)"
    )
    PlantPop: float = Field(description="Number of plants per hectare")
    PolColdStress: int = Field(description="pollination cold stress coefficient")
    PolHeatStress: int = Field(description="pollination heat stress coefficient")
    SeedSize: float = Field(
        description="Soil surface area (cm2) covered by an individual seedling at 90% emergence"
    )
    Senescence: float = Field(
        description="Growing degree/Calendar days from sowing to senescence"
    )
    SenescenceCD: Optional[float] = None
    SwitchGDD: int = Field(
        description="convert calendar to gdd mode if inputs are given in calendar days (0 = No; 1 = Yes)"
    )
    SxBotQ: float = Field(
        description="Maximum root water extraction at the bottom of the root zone (m3/m3/day) (page 108)"
    )
    SxTopQ: float = Field(
        description="Maximum root water extraction at top of the root zone (m3/m3/day) (page 108)"
    )
    Tbase: float = Field(
        description="base temperature (below which crop development does not progress) [degC] (page 21)"
    )
    Tmax_lo: float = Field(
        description="maximum air temperature (degC) at which pollination completely fails"
    )
    Tmax_up: float = Field(
        description="maximum air temperature (degC) above which pollination begins to fail"
    )
    Tmin_lo: float = Field(
        description="Minimum air temperature (degC) at which pollination completely fails"
    )
    Tmin_up: float = Field(
        description=" Minimum air temperature (degC) below which pollination begins to fail"
    )
    TrColdStress: int = Field(description="transpiration cold stress coefficient")
    Tupp: float = Field(
        description="upper temperature (above which crop development no longer increases with an increase in air temperature) [degC] (page 21)"
    )
    WP: float = Field(
        description="Water productivity normalized for ET0 and C02 (g/m2)"
    )
    WPy: float = Field(
        description="Adjustment of water productivity in yield_ formation stage (% of WP)"
    )
    YldForm: float = Field(
        description="duration of yield_ formation in growing degree/calendar days"
    )
    YldFormCD: Optional[float] = None
    Zmax: float = Field(description="Maximum effective rooting depth (m)")
    Zmin: float = Field(description="Minimum effective rooting depth (m)")
    a_HI: float = Field(
        description="harvest index crop parameter a (page 145)", ge=0.5, le=40
    )
    b_HI: float = Field(
        description="harvest index crop parameter b (page 147)", ge=1, le=20
    )
    dHI0: float = Field(
        description="Maximum allowable increase of harvest index above reference value"
    )
    dHI_pre: float = Field(
        description="Possible increase of harvest index due to water stress before flowering (%)"
    )
    exc: float = Field(description="excess of potential fruits")
    fage: float = Field(
        description="decline of crop coefficient due to ageing (%/day) (page 95)"
    )
    fshape_r: float = Field(description="shape factor describing root expansion")
    fshape_w1: float = Field(
        description="Shape factor describing water stress effects on canopy expansion"
    )
    fshape_w2: float = Field(
        description="Shape factor describing water stress effects on canopy expansion"
    )
    fshape_w3: float = Field(
        description="Shape factor describing water stress effects on canopy expansion"
    )
    fshape_w4: int = Field(
        description="Shape factor describing water stress effects on canopy expansion"
    )
    fsink: float = Field(
        description="Lower soil water depletion threshold for water stress effects on canopy expansion"
    )
    p_lo1: float = Field(
        description="Lower soil water depletion threshold for water stress effects on canopy expansion"
    )
    p_lo2: float = Field(
        description="Lower soil water depletion threshold for water stress effects on canopy expansion"
    )
    p_lo3: float = Field(
        description="Lower soil water depletion threshold for water stress effects on canopy expansion"
    )
    p_lo4: float = Field(
        description="Lower soil water depletion threshold for water stress effects on canopy expansion"
    )
    p_up1: float = Field(
        description="Upper soil water depletion threshold for water stress effects on affect canopy expansion"
    )
    p_up2: float = Field(
        description="Upper soil water depletion threshold for water stress effects on affect canopy expansion"
    )
    p_up3: float = Field(
        description="Upper soil water depletion threshold for water stress effects on affect canopy expansion"
    )
    p_up4: float = Field(
        description="Upper soil water depletion threshold for water stress effects on affect canopy expansion"
    )


def _get_aquacrop_names():
    return list(crop_params.keys())


def get_all_crop_data() -> List[HeliostromeCrop]:
    return [
        HeliostromeCrop(**crop_params[crop_name]) for crop_name in _get_aquacrop_names()
    ]


def get_crop_data(crop_name: str) -> HeliostromeCrop:
    return HeliostromeCrop(**crop_params[crop_name])
