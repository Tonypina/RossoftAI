from collections import defaultdict
from io import StringIO
import pickle
import pandas as pd
from rossoft.settings import MEDIA_ROOT
import numpy as np
import graphviz
import scipy.cluster.hierarchy as shc
from scipy.spatial import distance
from scipy.spatial.distance import cdist
from apyori import apriori
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import classification_report, mean_squared_error, mean_absolute_error, r2_score
from kneed import KneeLocator
from sklearn import linear_model, model_selection
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_graphviz
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import pydotplus
import matplotlib.pyplot as plt

from django.core.files.storage import default_storage

class Algorithms:

    def __init__( self, dataFile, algthm_type ):

        if algthm_type == 'apriori':
            self.__data = pd.read_csv( dataFile, header=None )    
        else:
            self.__data = pd.read_csv( dataFile )    

    def __save_model( self, model ):

        with default_storage.open('rossoftai/models/model.pkl', mode='wb') as model_pkl:
            pickle.dump(model, model_pkl)

    def __plot_tree( self, model, predictoras, y_clas ):
        dot_data = StringIO()
        export_graphviz(model, out_file=dot_data, feature_names=predictoras, class_names=y_clas)

        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())

        graph.write_png(MEDIA_ROOT+'/rossoftai/images/tree.png')

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

        return (CorrData, MatrizInf, list(self.__data.columns.values) )

    def __scaler( self, carac ):
        Matriz = np.array(self.__data[carac])

        estandarizar = StandardScaler()
        MEstandarizada = estandarizar.fit_transform(Matriz)
        
        return MEstandarizada

    def plot_dendrogram( self, carac, metric ):

        plt.figure(figsize=(10, 7))
        plt.xlabel('Observaciones')
        plt.ylabel('Distancia')
        
        Arbol = shc.dendrogram(shc.linkage(self.__scaler(carac), method='complete', metric=metric))
        plt.savefig(MEDIA_ROOT+'/rossoftai/images/dendrogram.png',figsize=(10, 8), dpi=300)



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

    def regression( self, clase, predictoras ):
        muestra = self.__data.at[0, clase]

        if ( isinstance(muestra, str) ):
            GroupByData = self.__data.groupby(clase)
            tempdict = {}

            for i, key in enumerate(GroupByData.indices.keys()):
                tempdict[key] = i
        
            self.__data = self.__data.replace(tempdict)
        
        X = np.array(self.__data[predictoras])
        Y = np.array(self.__data[[clase]])

        X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=0.2, random_state=1234, shuffle=True)
        Clasificacion = linear_model.LogisticRegression()
        Clasificacion.fit(X_train, Y_train)
        
        Y_Clasificacion = Clasificacion.predict(X_validation)

        Score = Clasificacion.score(X_validation, Y_validation)
        Matriz_Clasificacion = pd.crosstab(Y_validation.ravel(), Y_Clasificacion, rownames=['Real'], colnames=['Clasificación'])
        Reporte = classification_report(Y_validation, Y_Clasificacion)
        Intercepto = Clasificacion.intercept_
        Coeficientes = Clasificacion.coef_

        tempdict = {v: k for k, v in tempdict.items()}

        self.__save_model(Clasificacion)

        return (Score, Matriz_Clasificacion.to_json(orient='records'), Intercepto, Coeficientes, tempdict)

    def tree_classifier( self, clase, predictoras, max_depth, min_samples_split, min_samples_leaf ):
        X = np.array(self.__data[predictoras])
        Y = np.array(self.__data[[clase]])

        X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=0.2, random_state=1234, shuffle=True)

        Clasificacion = DecisionTreeClassifier(max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf)
        Clasificacion.fit(X_train, Y_train)

        Y_Clasificacion = Clasificacion.predict(X_validation)

        Score = Clasificacion.score(X_validation, Y_validation)
        Matriz_Clasificacion = pd.crosstab(Y_validation.ravel(), Y_Clasificacion, rownames=['Real'], colnames=['Clasificación'])

        self.__save_model( Clasificacion )

        self.__plot_tree( Clasificacion, predictoras, Y_Clasificacion )

        return (Score, Matriz_Clasificacion.to_json(orient='records'))
    
    def tree_regression( self, clase, predictoras, max_depth, min_samples_split, min_samples_leaf ):
        X = np.array(self.__data[predictoras])
        Y = np.array(self.__data[[clase]])

        X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=0.2, random_state=1234, shuffle=True)

        Pronostico = DecisionTreeRegressor(max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, random_state=0, criterion='absolute_error')
        Pronostico.fit(X_train, Y_train)

        Y_Pronostico = Pronostico.predict(X_test)

        Params = {}
        Params['Score'] = r2_score(Y_test, Y_Pronostico)
        Params['MAE'] = mean_absolute_error(Y_test, Y_Pronostico)
        Params['MSE'] = mean_squared_error(Y_test, Y_Pronostico)
        Params['RMSE'] = mean_squared_error(Y_test, Y_Pronostico, squared=False)

        self.__save_model( Pronostico )

        self.__plot_tree( Pronostico, predictoras, Y_Pronostico )

        return (Y_test, Y_Pronostico, Params, Pronostico.feature_importances_)
    
    def forest_regression( self, clase, predictoras, max_depth, min_samples_split, min_samples_leaf, estimators, estimator_viz ):
        X = np.array(self.__data[predictoras])
        Y = np.array(self.__data[[clase]])

        X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=0.2, random_state=1234, shuffle=True)

        Pronostico = RandomForestRegressor(n_estimators=estimators, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, random_state=0, criterion='absolute_error')
        Pronostico.fit(X_train, Y_train)

        Y_Pronostico = Pronostico.predict(X_test)

        Params = {}
        Params['Score'] = r2_score(Y_test, Y_Pronostico)
        Params['MAE'] = mean_absolute_error(Y_test, Y_Pronostico)
        Params['MSE'] = mean_squared_error(Y_test, Y_Pronostico)
        Params['RMSE'] = mean_squared_error(Y_test, Y_Pronostico, squared=False)

        self.__save_model( Pronostico )

        self.__plot_tree( Pronostico.estimators_[estimator_viz], predictoras, Y_Pronostico )

        return (Y_test, Y_Pronostico, Params, Pronostico.feature_importances_)

    def forest_classifier( self, clase, predictoras, max_depth, min_samples_split, min_samples_leaf, estimators, estimator_viz ):
        X = np.array(self.__data[predictoras])
        Y = np.array(self.__data[[clase]])

        X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=0.2, random_state=1234, shuffle=True)

        Clasificacion = RandomForestClassifier(n_estimators=estimators, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, random_state=0)
        Clasificacion.fit(X_train, Y_train)

        Y_Clasificacion = Clasificacion.predict(X_validation)

        Score = Clasificacion.score(X_validation, Y_validation)
        Matriz_Clasificacion = pd.crosstab(Y_validation.ravel(), Y_Clasificacion, rownames=['Real'], colnames=['Clasificación'])

        self.__save_model( Clasificacion )

        self.__plot_tree( Clasificacion.estimators_[estimator_viz], predictoras, Y_Clasificacion )

        return (Score, Matriz_Clasificacion.to_json(orient='records'))
        

    def predict( self, predictoras, values ):

        with default_storage.open('rossoftai/models/model.pkl', mode='rb') as model_pkl:
            model = pickle.load(model_pkl)

        x = {}
        i = 0

        while i < len(predictoras):
            x[predictoras[i]] = [values[i]]
            i = i + 1

        x_df = pd.DataFrame(x)
        prediccion = model.predict(x_df)

        return prediccion
