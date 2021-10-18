import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import os

csv_path = r"C:\Users\barisoztas\Desktop\CE-STAR\danish_lakes\Salinity\all_lakes\Danish_lakes_7days_results_v3.xlsx"
write_path= r"C:\Users\barisoztas\Desktop\CE-STAR\danish_lakes\Report\Figures"

def read_data(excel_file,sheet_name_rs,sheet_name_field):
    merged = pd.read_excel(excel_file, sheet_name=sheet_name_rs, engine='openpyxl')
    complete_dataset = pd.read_excel(excel_file, sheet_name=sheet_name_field, engine='openpyxl')
    merged = merged[merged["Type"].isin(["Shoreline"])]
    # Complete field data
    complete_salinity = complete_dataset["sal__permi"]
    complete_suspended_solid = complete_dataset["Susp_solid"]
    complete_chlorophyl = complete_dataset["Chlorophyl"]
    complete_water_temp = complete_dataset["temp_water"]
    complete_lake_names = complete_dataset["Lake Name"]
    complete_date = complete_dataset["Date"]
    complete_mean_depth = complete_dataset["Meandep_m"]
    comple_max_depth = complete_dataset["Maxdepth_m"]
    complete_area = complete_dataset["Area_ha"]

    # Merged Remote Sensing And Field data

    lake_names = merged["LakeName"]
    salinity = merged["sal__permi"]
    mean_depth = merged["Meandep_m"]
    max_depth = merged["Maxdepth_m"]
    chlorophyl = merged["Chlorophyl"]
    suspended_solid = merged["Susp_solid"]
    date = merged["Date"]
    B1 = merged["B1"]
    B2 = merged["B2"]
    B3 = merged["B3"]
    B4 = merged["B4"]
    B5 = merged["B5"]
    B6 = merged["B6"]
    B7 = merged["B7"]
    B10 = merged["B10"]
    B11 = merged["B11"]
    salinity_index = merged["Salinity Index"]
    temperature = merged["Air Temperature 2m (Celcius Degree)"]
    wind = merged["Resultant Wind (m/s)"]
    type = merged["Type"]

    return  complete_salinity, complete_suspended_solid, complete_chlorophyl, complete_water_temp, complete_lake_names, \
            complete_date, complete_mean_depth, comple_max_depth, complete_area, lake_names, salinity, mean_depth,\
            max_depth, chlorophyl, suspended_solid, date, B1, B2, B3, B4, B5, B6, B7, B10, B11, salinity_index, \
            temperature, wind, type

def create_histogram_and_write(list,list_string,average_list,write_path):
    plt.figure()
    fig, axs = plt.subplots(len(list), 1, tight_layout=True)
    for count in range(len(list)):
        axs[count].hist(list[count],bins=128)
        name = list_string[count]
        axs[count].set_title(name)
    fig = plt.gcf()
    fig.set_size_inches(18.5, 20.5)
    fig.savefig(os.path.join(write_path,"Histogram of Label Datas"), dpi=1000)
    plt.show()

def get_average(data_list):
    average_list =[]
    for data in data_list:
        data = data.to_numpy()
        average_list.append(np.average(data))
    return average_list

def create_label_list(data_list,avgs):
    label_list = []
    for count in range(len(avgs)):
        label_list.append(data_list[count]<= avgs[count])
    return label_list

def scatter_plot(salinity,x_list,label_list,list_string,avg_list,wind):
    salinity_index = (x_list[6]-x_list[4])/(x_list[6]+x_list[4])
    salinity_index.name = "Salinity Index"
    x_list.append(salinity_index)
    wind.name = "Wind (ms^-1)"
    x_list.append(wind)
    y_list = [salinity,suspended_solid]
    for y in y_list:
        for x in x_list:
            for count in range(len(label_list)):
                band_measured = pd.concat([x,y],axis=1)
                label_name_less = list_string[count] + " less than " + str(avg_list[count])
                label_name_greater = list_string[count] + " greater than " + str(avg_list[count])
                plt.plot(band_measured[label_list[count]==1].to_numpy()[:,0],
                         band_measured[label_list[count]==1].to_numpy()[:,1],'o',label = label_name_less,marke rsize = 3)
                plt.plot(band_measured[label_list[count]==0].to_numpy()[:,0],
                         band_measured[label_list[count]==0].to_numpy()[:,1],'o',label=label_name_greater,markersize = 3)
                plt.ylabel(y.name)
                plt.xlabel(x.name)
                plt.xlim(0,300)
                plt.title(x.name + " Values vs " + y.name)
                plt.legend()
                fig = plt.gcf()
                fig_name = x.name + '-'+y.name+'('+ list_string[count] + ")"
                fig.savefig(os.path.join(write_path,fig_name),dpi=300)
                plt.show()
    return

complete_salinity, complete_suspended_solid, complete_chlorophyl, complete_water_temp, complete_lake_names,\
complete_date, complete_mean_depth, comple_max_depth, complete_area, lake_names, salinity, mean_depth,max_depth, \
chlorophyl, suspended_solid, date, B1, B2, B3, B4, B5, B6, B7, B10, B11, salinity_index,temperature, wind, type = read_data(csv_path, "Merged", "Complete Field Dataset")
list = [salinity,suspended_solid, chlorophyl,mean_depth,wind]
list_string = ["Salinity", "Suspended Solid", "Chlorophyl", "Mean Depth (m)","Wind (ms^-1)"]
average_list = get_average(list)
create_histogram_and_write(list,list_string,average_list,write_path)
label_list = create_label_list(list,average_list)
y_list = [B1,B2,B3,B4,B5,B6,B7,B10,B11]
scatter_plot(salinity,y_list,label_list,list_string,average_list,wind)
a = 1