import pandas as pd
import os
import glob
from datetime import datetime as dt


csv_path = r"C:\Users\barisoztas\Desktop\CE-STAR\danish_lakes\Salinity\Salinity_index_values_csv"
output_path = r"C:\Users\barisoztas\Desktop\CE-STAR\danish_lakes\Salinity"

csv_list = sorted(list(glob.iglob(os.path.join(csv_path, '**', '*.csv'), recursive=True)))
salinity_index_list = []
for lake in csv_list:
    data = pd.read_csv(lake)
    system_index = data["system:index"].tolist()
    sat_name = []
    date = []
    base_lake_name_list = []
    lake_name = os.path.split(lake)[-1].split(".csv")[0]
    base_lake_name = lake_name.split("_")[0:-1]
    base_lake_name = " ".join(base_lake_name).capitalize()
    median = data["median"].tolist()
    for i in range(len(system_index)):
        base_lake_name_list.append(base_lake_name)
        sat_name.append(system_index[i].split("_",5)[1])
        current_date = dt.strptime(system_index[i].split("_",5)[3],'%Y%m%d')
        current_date = current_date.date()
        date.append(current_date)
    salinity ={'Satellite Name': sat_name,'Lake Name':base_lake_name_list, 'Date': date, 'Salinity Index': median}
    salinity = pd.DataFrame(data=salinity)
    salinity_index_list.append(salinity)


writer = pd.ExcelWriter(os.path.join(output_path,'Danish_lakes_rs_dataset.xlsx'),engine='xlsxwriter')
i=-1
for current in salinity_index_list:
    i = i+1
    lake_name = os.path.split(csv_list[i])[-1].split(".csv")[0]
    current.to_excel(writer,sheet_name=lake_name,index=False)
writer.save()








