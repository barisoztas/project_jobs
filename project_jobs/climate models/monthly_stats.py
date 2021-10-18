import numpy as np
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from matplotlib.pyplot import figure
from scipy.stats import pearsonr

def reading(folder):
    models_found =  sorted(list(glob.iglob(os.path.join(folder,"pr_*"),recursive=True)))
    return models_found



def get_names(models_found):
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
        (data[i])["Burdur"]=(data[i])["Burdur"]*86400
        data[i]["Month"]= data[i][["year", "month"]].astype(str).agg(''.join, axis=1)
        data[i]['Month'] = pd.to_datetime(data[i]['Month'], format='%Y%m')
        data[i] = (data[i])[["Burdur","Month"]]
        data[i] = data[i].groupby("Month",as_index=False).agg(
            {
                "Burdur":sum
            }
        )
        data[i].columns = ["Month", names[i]]
        data[i].index = data[i]["Month"]
        i=i+1
    merged_models = data[0]
    for i in range(len(names)-1):
        merged_models = merged_models.join(data[i+1][names[i+1]])

    return merged_models


def merge(model_prep,xlsx_path_prep,names):
    prep = pd.read_excel(xlsx_path_prep)
    burdur_prep = prep[prep["Istasyon_Adi"].isin(["Burdur"])][["prep","Month"]]
    burdur_prep['Month'] = pd.to_datetime(burdur_prep['Month'], format='%Y%m',errors='coerce').dropna()
    burdur_prep.columns=["Burdur Yagis Istasyon(kg/m^2)","Month"]
    burdur_prep.index = burdur_prep["Month"]
    del(prep)
    merged_prep = model_prep.join(burdur_prep["Burdur Yagis Istasyon(kg/m^2)"])
    merged_prep['Year'] = merged_prep["Month"].dt.year
    names.append("Burdur Yagis Istasyon(kg/m^2)")
    yearly = merged_prep.groupby('Year')[names].sum()
    return merged_prep,yearly

def writing(merged_prep,yearly,write_path):
    merged_prep.to_excel(os.path.join(write_path,"rcp85.xlsx"),index=False)
    yearly.to_excel(os.path.join(write_path,"rcp85_yearly.xlsx"),index=True)

def scatter(folder,names):
    monthly_path = os.path.join(folder,'rcp85.xlsx')
    yearly_path = os.path.join(folder,'rcp85_yearly.xlsx')
    figure_folder = r"C:\Users\barisoztas\Desktop\CE-STAR\CORDEX\version_3\rcp85_burdur\figures"
    monthly = pd.read_excel(monthly_path,parse_dates=["Month"])
    yearly = pd.read_excel(yearly_path,parse_dates=["Year"])
    names.append("Burdur Yagis Istasyon(kg/m^2)")
    for i in range(len(names)-1):
        measured = yearly["Burdur Yagis Istasyon(kg/m^2)"].to_numpy()
        model = yearly[names[i]].to_numpy()
        model = model[~np.isnan((measured))]
        measured = measured[~np.isnan(measured)]
        measured = measured[~np.isnan(model)]
        model = model[~np.isnan((model))]
        plt.scatter(measured,model)
        plt.xlabel("Measured (kg/m^2)")
        plt.ylabel("Model (kg/m^2)")
        corr, _ = pearsonr(measured,model)
        plt.title(names[i].split(".")[0]+ '      (yearly)'+'    Pearson R: ' + str(corr))
        fig = plt.gcf()
        fig.set_size_inches(18.5, 18.5)
        fig.savefig(os.path.join(figure_folder,names[i].split(".")[0]), dpi=100)
        plt.show()

def time_series(folder,names):
    monthly_path = os.path.join(folder,'historic.xlsx')
    yearly_path = os.path.join(folder,'historic_yearly.xlsx')
    figure_folder = r"C:\Users\barisoztas\Desktop\CE-STAR\CORDEX\version_3\rcp85_burdur\figures"
    monthly = pd.read_excel(monthly_path,parse_dates=["Month"])
    yearly = pd.read_excel(yearly_path,parse_dates=["Year"])
    names.append("Burdur Yagis Istasyon(kg/m^2)")
    for i in range(len(names)-1):
        measured = yearly["Burdur Yagis Istasyon(kg/m^2)"].to_numpy()
        model = yearly[names[i]].to_numpy()
        fig, axs = plt.subplots(figsize=(12, 4))
        model = model[~np.isnan((measured))]
        dates = yearly["Year"][~np.isnan(measured)].dt.year.to_numpy()
        # model = model[~np.isnan(model)]
        measured = measured[~np.isnan(measured)]
        plt.bar(x=dates+0.3,height=measured,width=0.3,label='Station Yearly Sum',align='center')
        plt.bar(x=dates,height=model,width=0.3,label=names[i].split('.')[0]+ ' Yearly Sum',align='center')
        plt.title('Yearly')
        plt.xlabel('Date')
        plt.ylabel('Precipitation (kg/m^2)')
        plt.legend()
        fig.show()
        fig.savefig(os.path.join(figure_folder,names[i].split(".")[0]), dpi=300)
        a=1



folder = r"C:\Users\barisoztas\Desktop\CE-STAR\CORDEX\version_3\rcp85_burdur"
prec_xlsx = r"C:\Users\barisoztas\Desktop\CE-STAR\CORDEX\version_3\rcp85_burdur\Aylik_yagis.xlsx"
files = reading(folder)
names = get_names(files)
# data = prec_cm(files,names)
# merged,yearly = merge(data,prec_xlsx,names)
# writing(merged,yearly,folder)
# scatter(folder,names)
time_series(folder,names)
