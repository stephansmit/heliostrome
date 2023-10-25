import pandas as pd
import os
from modules.waterflux_extraction import clean_excel_file

file_paths = [
    {"input": r"heliostrome/jip_project/results/WaterFlux_moroccoWheat.xlsx", "output": r"heliostrome/jip_project/results/cleaned_WaterFlux_morocco.xlsx"},
    {"input": r"heliostrome/jip_project/results/WaterFlux_Bangladesh.xlsx", "output": r"heliostrome/jip_project/results/cleaned_WaterFlux_Bangladesh.xlsx"},
    {"input": r"heliostrome/jip_project/results/WaterFlux_northeastCHINA.xlsx", "output": r"heliostrome/jip_project/results/cleaned_WaterFlux_NorthEastCHINA.xlsx"},
    #{"input": r"heliostrome/jip_project/results/WaterFlux_IranPotato.xlsx", "output": r"heliostrome/jip_project/results/cleaned_WaterFlux_IranPotato.xlsx"},
    # Add more file pairs as needed
]

for file_info in file_paths:
    input_path = file_info["input"]
    output_path = file_info["output"]
    clean_excel_file(input_path, output_path)
