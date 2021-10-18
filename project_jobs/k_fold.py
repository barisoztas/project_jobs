import os
import pandas as pd
import numpy as np



csv_path = r"C:\Users\barisoztas\Desktop\CE-STAR\danish_lakes\Machine_Learning\mars_folder\Version4\danish_lakes_l5_l8_merged_with_CV_Index.xlsx"
write_path = r"C:\Users\barisoztas\Desktop\CE-STAR\danish_lakes\Machine_Learning\mars_folder\Version4"
def read_data_sample_l5_export_x_y(csv_path):
    merged = pd.read_excel(csv_path, sheet_name="danish_lakes_l5_l8_merged_with_",engine="openpyxl")
    merged["B1"] = np.array(merged["B1"].tolist()) / 10000
    merged["B2"] = np.array(merged["B2"].tolist()) / 10000
    merged["B3"] = np.array(merged["B3"].tolist()) / 10000
    merged["B4"] = np.array(merged["B4"].tolist()) / 10000
    merged["B5"] = np.array(merged["B5"].tolist()) / 10000
    merged["B6"] = np.array(merged["B6"].tolist()) / 10
    merged["B7"] = np.array(merged["B7"].tolist()) / 10000
    merged["Salinity_Index"] = (merged["B7"]-merged["B4"])/(merged["B7"]+merged["B4"])
    x = merged[["sal_permi","CV_Index"]]
    group1 = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "Air_Temperature", "Wind",
              "Salinity_Index","CV_Index"]
    group2 = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "Salinity_Index", "Air_Temperature",
              "Wind", "Susp_solid", "Chlorophyl", "Temp_water", "Meandep_m","CV_Index"]
    y_1 = merged[group1]
    y_2 = merged[group2]
    return x,y_1,y_2

def read_data_sample_l8_export_x_y(csv_path):
    merged = pd.read_excel(csv_path, sheet_name="Sheet1",engine="openpyxl")
    merged["B1"] = np.array(merged["B1"].tolist()) / 10000
    merged["B2"] = np.array(merged["B2"].tolist()) / 10000
    merged["B3"] = np.array(merged["B3"].tolist()) / 10000
    merged["B4"] = np.array(merged["B4"].tolist()) / 10000
    merged["B5"] = np.array(merged["B5"].tolist()) / 10000
    merged["B6"] = np.array(merged["B6"].tolist()) / 10000
    merged["B7"] = np.array(merged["B7"].tolist()) / 10000
    merged["B10"] = np.array(merged["B10"].tolist()) / 10
    merged["Salinity_Index"] = (merged["B7"]-merged["B5"])/(merged["B7"]+merged["B5"])
    x = merged["sal_permi","CV_Index"]
    group1 = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B10", "Air Temperature 2m (Celcius Degree)",
              "Resultant Wind (m/s)", "Salinity_Index","CV_Index"]
    group2 = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B10", "Salinity_Index", "Air Temperature 2m (Celcius Degree)",
              "Resultant Wind (m/s)", "Susp_solid", "Chlorophyl", "temp_water", "Meandep_m","CV_Index"]
    y_1 = merged[group1]
    y_2 = merged[group2]
    return x,y_1,y_2

def writing_merged(y,x_1,x_2,write_path):
    y.to_csv(os.path.join(write_path,"y.csv"),index=False)
    x_1.to_csv(os.path.join(write_path, "x_1.csv"), index=False)
    x_2.to_csv(os.path.join(write_path, "x_2.csv"), index=False)


y,x_1,x_2 = read_data_sample_l5_export_x_y(csv_path)
writing_merged(y,x_1,x_2,write_path)