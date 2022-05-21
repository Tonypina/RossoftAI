import os
from statistics import mode
from urllib import response
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

from django.core.files.storage import default_storage

from .models import Data, Report
from .serializers import DataSerializer, ReportSerializer

from .algorithms import Algorithms

import json

class ReportListView(APIView):
    def get(self, request, *args, **kwargs):
        reports = Report.reportobjects.all()

        serializer = ReportSerializer(reports, many=True)

        return Response(serializer.data)

class AlgorithmView(APIView):
    parser_classes = (FileUploadParser,)
    
    def post(self, request):
    
        data = request.data.get('file', None)

        with default_storage.open('rossoftai/data/_'+data.name, mode='wb') as destination:
            for chunk in data.chunks():
                destination.write(chunk)

        with default_storage.open('rossoftai/data/_'+data.name, mode='r') as fp:
            lines = fp.readlines()

        with default_storage.open('rossoftai/data/_'+data.name, mode='w') as fp:
            for number, line in enumerate(lines):
                if number not in [0, 1, 2, 3, len(lines)-1]:
                    fp.write(line)

        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save()
            
            default_storage.delete('rossoftai/data/'+data.name)

            return Response(
                '_'+data.name,
                status=status.HTTP_201_CREATED)
        
        default_storage.delete('rossoftai/data/'+data.name)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        algthm = Algorithms( default_storage.open('rossoftai/data/'+request.query_params.get('name'), mode='rb'), request.query_params.get('algthm_type') )
        
        algthm_type = request.query_params.get('algthm_type')
        if ( algthm_type == 'apriori' ):

            return Response(
                (algthm.apriori_algorithm(
                    float(request.query_params.get('support')),
                    float(request.query_params.get('confidence')),
                    int(request.query_params.get('lift'))
                ),
                algthm.apriori_freq_dist()),
                status=status.HTTP_200_OK
            )
        elif ( algthm_type == 'metrics' ):

            return Response(
                algthm.metrics( 
                    request.query_params.get('metric'), 
                    request.query_params.get('lambda')
                ),
                status=status.HTTP_200_OK
            )
        elif ( algthm_type == 'distance' ):

            return Response(
                algthm.get_distance( 
                    request.query_params.get('metric'), 
                    request.query_params.get('lambda'),
                    int(request.query_params.get('obj_1')),
                    int(request.query_params.get('obj_2'))
                ),
                status=status.HTTP_200_OK
            )
        elif ( algthm_type == 'selec' ):

            return Response(
                algthm.caracteristic_selection(),
                status=status.HTTP_200_OK
            )
        elif ( algthm_type == 'hclust' ):

            return Response(
                algthm.h_clust(
                    int(request.query_params.get('nClust')),
                    json.loads(request.query_params.get('carac'))
                ),
                status=status.HTTP_200_OK
            )
        elif ( algthm_type == 'kmeans' ):

            return Response(
                algthm.k_means(
                    json.loads(request.query_params.get('carac'))
                ),
                status=status.HTTP_200_OK
            )
        elif ( algthm_type == 'pclust' ):

            return Response(
                algthm.p_clust(
                    int(request.query_params.get('nClust')),
                    json.loads(request.query_params.get('carac'))
                ),
                status=status.HTTP_200_OK
            )
        elif ( algthm_type == 'get_data' ):

            return Response(
                algthm.get_data(),
                status=status.HTTP_200_OK
            )
        elif ( algthm_type == 'regression' ):

            return Response(
                algthm.regression(
                    request.query_params.get('clase'),
                    json.loads(request.query_params.get('predictoras'))
                ),
                status=status.HTTP_200_OK
            )
        elif ( algthm_type == 'tree_classifier' ):

            return Response(
                algthm.tree_classifier(
                    request.query_params.get('clase'),
                    json.loads(request.query_params.get('predictoras')),
                    int(request.query_params.get('max_depth')),
                    int(request.query_params.get('min_samples_split')),
                    int(request.query_params.get('min_samples_leaf'))
                ),
                status=status.HTTP_200_OK
            )
        elif ( algthm_type == 'tree_regression' ):

            return Response(
                algthm.tree_regression(
                    request.query_params.get('clase'),
                    json.loads(request.query_params.get('predictoras')),
                    int(request.query_params.get('max_depth')),
                    int(request.query_params.get('min_samples_split')),
                    int(request.query_params.get('min_samples_leaf'))
                ),
                status=status.HTTP_200_OK
            )
        elif ( algthm_type == 'predict' ):

            return Response(
                algthm.predict(
                    json.loads(request.query_params.get('predictoras')),
                    json.loads(request.query_params.get('values'))
                ),
                status=status.HTTP_200_OK
            )
        elif ( algthm_type == 'get_tree' ):
            
            with default_storage.open('rossoftai/images/tree.png', mode='rb') as png:
                response = HttpResponse(png.read(), content_type='image/png')
                response['Content-Disposition'] = 'attachment; filename=tree.png'
                return response
