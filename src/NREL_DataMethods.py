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
    #cluster_info, k_means_info = k_cluster.k_means_clustering(k,df,item_attribs,class_attribute)
    #print("Total points: ", k_means_info[0])
    #print('Centroid: ', k_means_info[1])
    #print('Silhouette Coefficient: ', k_means_info[2])
    #print('H(U) = ', k_means_info[3])
    #print('H(V) = ', k_means_info[4])
    #print('MI(U, V) = ', k_means_info[5])
    #print('AMI(U, V) = ', k_means_info[6])
    #print('MIDIST(U,V) = ', k_means_info[7])
    #print('AMIDIST(U,V) = ', k_means_info[8])
    #for i in range(0, len(cluster_info)):
    #    print("Cluster: ", i, "; Histogram: ", cluster_info[i][2])
    #    for h in range(len(cluster_info[i][0])):
    #        print("Attribute: " + str(cluster_info[i][0][h]))
    #        print("Tendencies:")
    #        print("Median: " + str(cluster_info[i][1][h][0]))
    #       print("Mode: " + str(cluster_info[i][1][h][1]))
    #        print("Mean: " + str(cluster_info[i][1][h][2]))

    k_cluster.agglo_clustering(k, df)

