import numpy as np
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from matplotlib.pyplot import figure
from scipy.stats import pearsonr


def reading_temp(folder):
    models_found =  sorted(list(glob.iglob(os.path.join(folder,"tas_*"),recursive=True)))
    return models_found

def get_names_temp(models_found):
    model_names=[]
    names =[]
    for number in range(len(models_found)):
        model_names.append(models_found[number].split("\\")[-1])
        name = model_names[number].split("_")
        b = np.array([2,3, 4, 5,10,12])
        names.append([name[i] for i in b])
        names[number] = "_".join(names[number])
    return names

def prec_cm(models_found,names):
    data =[]
    i = 0
    for xlsx_path in models_found:
        data.append(pd.read_excel(xlsx_path,engine="openpyxl"))
        (data[i])["Burdur"]=(data[i])["Burdur"]
        data[i]["Month"]= data[i][["year", "month"]].astype(str).agg(''.join, axis=1)
        data[i]['Month'] = pd.to_datetime(data[i]['Month'], format='%Y%m')
        data[i] = (data[i])[["Burdur","Month"]]
        data[i] = data[i].groupby("Month",as_index=False).agg(
            {
                "Burdur":'mean'
            }
        )
        data[i].columns = ["Month", names[i]]
        data[i].index = data[i]["Month"]
        i=i+1
    merged_models = data[0]
    for i in range(len(names)-1):
        merged_models = merged_models.join(data[i+1][names[i+1]])

    return merged_models

def merge_temp(model_temp,xlsx_path_temp,names):
    temp = pd.read_excel(xlsx_path_temp)
    burdur_temp = temp[temp["Istasyon_Adi"].isin(["Burdur"])][["temp","Month"]]
    burdur_temp['Month'] = pd.to_datetime(burdur_temp['Month'], format='%Y-%m',errors='coerce').dropna()
    burdur_temp.columns=["Burdur Station","Month"]
    burdur_temp.index = burdur_temp["Month"]
    del(temp)
    merged_temp = model_temp.join(burdur_temp["Burdur Station"])
    merged_temp['Year'] = merged_temp["Month"].dt.year
    names.append("Burdur Station")
    yearly = merged_temp.groupby('Year')[names].mean()
    return merged_temp,yearly

def writing_temp(merged_temp,yearly,write_path):
    merged_temp.to_excel(os.path.join(write_path,"hist_temp.xlsx"),index=False)
    yearly.to_excel(os.path.join(write_path,"hist_yearly_temp.xlsx"),index=True)


folder = r"C:\Users\barisoztas\Desktop\CE-STAR\CORDEX\version_3\historical"
temp_xlsx = r"C:\Users\barisoztas\Desktop\CE-STAR\CORDEX\version_3\historical\Aylik_sıcaklık.xlsx"
files = reading_temp(folder)
names = get_names_temp(files)
# data = prec_cm(files,names)
# merged,yearly = merge_temp(data,temp_xlsx,names)
writing_temp(merged,yearly,folder)