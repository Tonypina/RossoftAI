import pandas as pd
from rossoft.settings import BASE_DIR, MEDIA_ROOT
import numpy as np
from apyori import apriori

class Algorithms:

    def __init__( self, dataType, dataURL ):

        if dataType == 'csv':
            self.__data = pd.read_csv( dataURL, header=None )
        elif dataType == 'xlsx':
            self.__data = pd.read_excel( '..'+dataURL )
        else:
            self.__data = None

    def apriori_freq_dist( self ):

        Transactions = self.__data.values.reshape(-1).toList()

        List = pd.DataFrame( Transactions )
        List['Frecuencia'] = 1

        List = List.groupby(by=[0], as_index=False).count().sort_values(by=['Frecuencia'], ascending=True)
        List['Porcentaje'] = (List['Frecuencia'] / List['Frecuencia'].sum())
        List = List.rename(columns={0 : 'Item'})

        return List
    
    def apriori_algorithm( self, support, confidence, lift ):

        # Pocesamiento
        List = self.__data.stack().groupby(level=0).apply(list).toList()

        Reglas = apriori(List, min_support=support, min_confidence=confidence, min_lift=lift)

        Resultados = list(Reglas)

        ResultadosJSON = pd.DataFrame(Resultados).to_json()

        return ResultadosJSON

    