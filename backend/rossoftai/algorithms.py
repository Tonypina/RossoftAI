from cmath import isnan
from ctypes.wintypes import COLORREF
import pandas as pd
import numpy as np
import seaborn as sns
import scipy.cluster.hierarchy as shc
from scipy.spatial import distance
from scipy.spatial.distance import cdist
from apyori import apriori
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.cluster import AgglomerativeClustering

from django.core.files.storage import default_storage

import matplotlib.pyplot as plt
# %matplotlib inline

class Algorithms:

    def __init__( self, dataFile ):
        # self.__data = pd.read_csv( dataFile, header=None )    
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
        # return List
    
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

    def scaler( self, carac ):
        Matriz = np.array(self.__data[carac])

        estandarizar = StandardScaler()
        MEstandarizada = estandarizar.fit_transform(Matriz)
        
        return MEstandarizada

    def h_clust( self, nClust, MEstandarizada ):

        MJerarquico = AgglomerativeClustering(n_clusters=nClust, linkage='complete', affinity='euclidean')
        MJerarquico.fit_predict(MEstandarizada)

        self.__data['clusterH'] = MJerarquico.labels_

        CentroidesH = self.__data.groupby('clusterH').mean()

        return CentroidesH