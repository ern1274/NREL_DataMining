import NREL_DataMining.src.apriori_NREL as apriori
import NREL_DataMining.src.Clustering_NREL as k_cluster
import pandas as pd

def prep_apriori(data):
    #data is array of panda Series, convert to Dataframe.
    df = pd.DataFrame(data)
    item_attribs = ['Month','Temperature','Wind Speed', 'DNI', 'GHI']
    minsup = 10
    lk = apriori.apriori(3, df, item_attribs, minsup)
    apriori.print_apriori_data(lk)

def prep_clustering(data):
    df = pd.DataFrame(data)
    item_attribs = ['Solar Zenith Angle','Temperature', 'GHI', 'DHI']
    class_attribute = 'DNI'
    k = 10
    k_cluster.k_means_clustering(k,df,item_attribs,class_attribute)
    k_cluster.agglo_clustering(k, df)

