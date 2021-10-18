import pandas as pd
import numpy as np
import seaborn
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import centroid_initialization as cent_init
import ckwrap

csv_path = r"C:\Users\barisoztas\Desktop\CE-STAR\danish_lakes\Salinity\all_lakes\Danish_lakes_7days_results_v3.xlsx"
kmeans = KMeans(n_clusters= 5)
def segmentation_label_creater(array,segmentation_number):
    label = ckwrap.ckmeans(array,segmentation_number).labels
    return label
def cluster_label_creater(data,number):
    kmeans = KMeans(
        n_clusters = number,init='k-means++',
        n_init=1,max_iter=1000)
    label = kmeans.fit(data)
    return label



# Read Data
merged = pd.read_excel(csv_path,sheet_name="Merged",engine='openpyxl')
complete_dataset = pd.read_excel(csv_path,sheet_name="Complete Field Dataset",engine='openpyxl')
filter_lake_names = ['Agger tange so', 'Ferring so', 'Gambor indrefjord', 'Gjeller so',
       'Harboore fjord', 'Hovedso', 'Hygum nor', 'Kallerup kaer',
       'Kettingnor', 'Kilen', 'Lonnerup fjord', 'Mellemvese',
       'Nakskov indrefjord', 'Orestrand', 'Orslevkloster so',
       'Osterild fjord', 'Skarre soer', 'Ulvedybet nord']
#filter_lake_names = ['Harboore fjord','Hygum nor','Ulvedybet nord','Kilen']

#merged = merged[merged["LakeName"].isin(filter_lake_names)]
merged = merged[merged["Type"].isin(["Shoreline"])]
# Get merged dataset and prepare data
lake_names = merged["LakeName"]
salinity_index = merged["Salinity Index"]
sal_permi = merged["sal__permi"]
mean_depth = merged["Meandep_m"]
chlorophyl = merged["Chlorophyl"]
suspended_solid = merged["Susp_solid"]
wind = merged["Resultant Wind (m/s)"]
sal_index_depth_scatter = pd.concat([mean_depth, salinity_index],axis=1)
index_measured = pd.concat([sal_permi,salinity_index],axis=1).to_numpy()

#cluster or segmentation type
# label = cluster_label_creater(index_measured,4).labels_
# u_labels = np.unique(label)
label = segmentation_label_creater(wind,3)
u_labels = np.unique(label)


# plotting the clustered data:
for i in u_labels:
    plt.plot(index_measured[label == i,0], index_measured[label == i,1] , 'o' , label = i)
    # z = np.polyfit(index_measured[label == i,0],index_measured[label == i,1],1)
    # p = np.poly1d(z)
    # print(p)
    # plt.plot(index_measured[label == i,0],p(index_measured[label == i,0]),"r--")
plt.ylim(-1,0)
plt.ylabel("Salinity Index")
plt.xlabel("Salinity Permi")
plt.title("SI - Salinity Measured \n Segmentation according to Wind")
plt.gca().invert_yaxis()
plt.legend()
plt.subplot()
plt.show()
plt.hist(chlorophyl)



