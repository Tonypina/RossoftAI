
import pandas as pd
import numpy as np
import seaborn as sns
import scipy.cluster.hierarchy as shc
from scipy.spatial import distance
from scipy.spatial.distance import cdist
from apyori import apriori
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from kneed import KneeLocator

from django.core.files.storage import default_storage

class Algorithms:

    def __init__( self, dataFile, algthm_type ):

        if algthm_type == 'apriori':
            self.__data = pd.read_csv( dataFile, header=None )    
        else:
            self.__data = pd.read_csv( dataFile )    

    def get_data( self ):
        return pd.DataFrame( self.__data ).to_json(orient='records')

    def apriori_freq_dist( self ):

        Transactions = self.__data.values.reshape(-1).tolist()

        List = pd.DataFrame( Transactions )
        List['Frecuencia'] = 1

        List = List.groupby(by=[0], as_index=False).count().sort_values(by=['Frecuencia'], ascending=True)
        List['Porcentaje'] = (List['Frecuencia'] / List['Frecuencia'].sum())
        List = List.rename(columns={0 : 'Item'})

        return List.to_json(orient='records')
    
    def apriori_algorithm( self, support, confidence, lift ):

        # Pocesamiento
        List = self.__data.stack().groupby(level=0).apply(list).tolist()

        Reglas = apriori(List, min_support=support, min_confidence=confidence, min_lift=lift)

        Resultados = list(Reglas)

        ResultadosDF = pd.DataFrame(Resultados)

        for r in Resultados:
            ResultadosDF['confidence'] = r.ordered_statistics[0][2]
            ResultadosDF['lift'] = r.ordered_statistics[0][3]

        ResultadosJSON = ResultadosDF.to_json(orient='records')

        return ResultadosJSON

    def metrics( self, metricType, lambdaParam ):

        if (lambdaParam == None):
            return pd.DataFrame(cdist(self.__data, self.__data, metric=metricType)).to_json(orient='records')
        else:
            return cdist(self.__data, self.__data, metric=metricType, p=float(lambdaParam))
    
    def get_distance( self, metricType, lambdaParam, obj_1, obj_2 ):

        if (lambdaParam == None):
            if (metricType == 'euclidean'):
                return distance.euclidean(self.__data.iloc[obj_1], self.__data.iloc[obj_2])
            elif (metricType == 'chebyshev'):
                return distance.chebyshev(self.__data.iloc[obj_1], self.__data.iloc[obj_2])
            elif (metricType == 'cityblock'):
                return distance.cityblock(self.__data.iloc[obj_1], self.__data.iloc[obj_2])
            elif (metricType == 'minkowski'):
                return distance.minkowski(self.__data.iloc[obj_1], self.__data.iloc[obj_2])
        else:
            return distance.minkowski(self.__data.iloc[obj_1], self.__data.iloc[obj_2])

    def caracteristic_selection( self ):

        CorrData = self.__data.corr(method='pearson')
        MatrizInf = np.triu(CorrData)

        return (CorrData, MatrizInf)

    def __scaler( self, carac ):
        Matriz = np.array(self.__data[carac])

        estandarizar = StandardScaler()
        MEstandarizada = estandarizar.fit_transform(Matriz)
        
        return MEstandarizada

    def h_clust( self, nClust, carac ):

        MEstandarizada = self.__scaler(carac)

        MJerarquico = AgglomerativeClustering(n_clusters=nClust, linkage='complete', affinity='euclidean')
        MJerarquico.fit_predict(MEstandarizada)

        self.__data['cluster'] = MJerarquico.labels_

        CentroidesH = self.__data.groupby('cluster').mean()

        return (self.__data.to_json(orient='records'), CentroidesH.to_json(orient='records'))
    
    def k_means( self, carac ):
        MEstandarizada = self.__scaler(carac)

        SSE = []
        for i in range(2, 12):
            km = KMeans(n_clusters=i, random_state=0)
            km.fit(MEstandarizada)
            SSE.append(km.inertia_)

        kl = KneeLocator(range(2,12), SSE, curve="convex", direction="decreasing")

        return (SSE, kl.elbow)

    def p_clust( self, nClust, carac ):

        MEstandarizada = self.__scaler(carac)

        MParticional = KMeans(n_clusters=nClust, random_state=0).fit(MEstandarizada)
        MParticional.predict(MEstandarizada)

        self.__data['cluster'] = MParticional.labels_

        CentroidesP = self.__data.groupby('cluster').mean()

        return (self.__data.to_json(orient='records'), CentroidesP.to_json(orient='records'))