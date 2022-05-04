from statistics import mode
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

from django.core.files.storage import default_storage

from .models import Data, Report
from .serializers import DataSerializer, ReportSerializer

from .algorithms import Algorithms

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
            
            return Response(
                '_'+data.name,
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        algthm = Algorithms( default_storage.open('rossoftai/data/'+request.query_params.get('name'), mode='rb') )
        
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
                algthm.metrics( request.query_params.get('metricType') ),
                status=status.HTTP_200_OK
            )
        elif ( algthm_type == 'selec' ):

            return Response(
                algthm.caracteristic_selection(),
                status=status.HTTP_200_OK
            )
        elif ( algthm_type == 'hclust' ):

            return Response(
                algthm.h_clust(),
                status=status.HTTP_200_OK
            )
        elif ( algthm_type == 'get_data' ):

            return Response(
                algthm.get_data(),
                status=status.HTTP_200_OK
            )
