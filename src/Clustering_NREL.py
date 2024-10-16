import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OrdinalEncoder, normalize
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score, mutual_info_score, adjusted_mutual_info_score
from scipy.stats import entropy
import scipy.cluster.hierarchy as shc
import ctypes
import os

so_file = os.getcwd() + '/analyze.so'
cMethods = ctypes.CDLL(so_file)

def print_kmeans_data(df):
    for index, row in df.iterrows():
        print(row)
def k_means_clustering_draft(k, df, attributes, class_attribute):
    df = df.dropna()
    scaled_df = StandardScaler().fit_transform(df)
    kmeans_kwargs = {
        "init": "random",
        "n_init": 10,
        "random_state": 1,
    }
    sse = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(scaled_df)
        sse.append(kmeans.inertia_)

    # visualize results
    plt.plot(range(1, 11), sse)
    plt.xticks(range(1, 11))
    plt.xlabel("Number of Clusters")
    plt.ylabel("SSE")
    plt.show()
    kmeans = KMeans(init="random", n_clusters=8, n_init=10, random_state=1)

    # fit k-means algorithm to data
    kmeans.fit(scaled_df)
    df['cluster'] = kmeans.labels_

    # view updated DataFrame
    print_kmeans_data(df)


def cluster_central_tendency(df):
    for attribute in df.keys():
        print("Attribute: " + attribute)
        values = df[attribute].values
        length = len(values)
        c_array_type = ctypes.c_double * length
        arr = c_array_type(*values)

        cMethods.centralTendency.argtypes = [ctypes.Array, ctypes.c_int]

        cMethods.centralTendency(arr, length)
        print("\n")
def k_means_clustering(k, df, attributes, class_attribute):
    # Data must be scaled due to the difference in potential x-axis values and y-axis values
    # A Min Max Scaler is an option
    min_max_scaler = MinMaxScaler()

    for a in attributes:
        df[a] = pd.DataFrame(min_max_scaler.fit_transform(df[a].to_frame()))

    kmeans_kwargs = {
        "init": "random",
        "n_init": 10,
        "random_state": 1,
    }
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    k_clustering = kmeans.fit(df[attributes])
    print('Centroid: ', k_clustering.cluster_centers_)


    total_points = 0
    for current_cluster in range(0, k):
        points_assigned = df.iloc[(k_clustering.labels_ == current_cluster).nonzero()]
        df['Cluster'] = k_clustering.labels_
        cluster_central_tendency(points_assigned)

        total_points += len(points_assigned)
        histogram = points_assigned[class_attribute].value_counts(sort=False)
        print("Cluster: ", current_cluster, "; Histogram: ", histogram)
    print("Total points: ", total_points)

    # Now silhouette points
    sc = silhouette_score(df[attributes], k_clustering.labels_)

    print('Silhouette Coefficient: ', sc)

    # Entropy using ground truth
    encoder = OrdinalEncoder()
    # ground_truth_labels = encoder.fit_transform(spotify_df[[class_attrib_spotify]])[:, 0]
    ground_truth_labels = encoder.fit_transform(df[[class_attribute]])[:, 0]

    print('length of ground truth labels: ', len(ground_truth_labels))
    u, v = k_clustering.labels_, ground_truth_labels
    hu, hv = entropy(u), entropy(v)

    print('H(U) = ', hu)
    print('H(V) = ', hv)
    # Now getting the mutual information score
    mi, ami = mutual_info_score(u, v), adjusted_mutual_info_score(u, v)
    print('MI(U, V) = ', mi)
    print('AMI(U, V) = ', ami)


    mi_dist_uv, ami_dist_uv = 1 - (mi / max(hu, hv)), 1 - (ami / max(hu, hv))
    print('MIDIST(U,V) = ', mi_dist_uv)
    print('AMIDIST(U,V) = ', ami_dist_uv)

def agglo_clustering(k, df):
    stand_scaler = StandardScaler()

    X_scaled = stand_scaler.fit_transform(df)

    X_normalized = normalize(X_scaled)
    X_normalized = pd.DataFrame(X_normalized)

    pca = PCA(n_components=2)
    X_principal = pca.fit_transform(X_normalized)
    X_principal = pd.DataFrame(X_principal)
    X_principal.columns = ['P1', 'P2']

    plt.figure(figsize=(8, 8))
    plt.title('Visualising the data')
    Dendrogram = shc.dendrogram((shc.linkage(X_principal, method='ward')))

    ac2 = AgglomerativeClustering(n_clusters=k)

    # Visualizing the clustering
    plt.figure(figsize=(6, 6))
    plt.scatter(X_principal['P1'], X_principal['P2'],
                c=ac2.fit_predict(X_principal), cmap='rainbow')
    plt.show()


