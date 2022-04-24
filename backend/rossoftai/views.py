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

class UploadDataView(APIView):
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
                if number not in [0, 1, 2, 3]:
                    fp.write(line)

        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save()

            algthm = Algorithms( default_storage.open('rossoftai/data/_'+data.name, mode='rb') )
            # algthm = Algorithms(  default_storage.open('rossoftai/data/movies.csv', mode='rb') )

            return Response(
                algthm.apriori_algorithm( 0.01, 0.3, 2 ),
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AprioriView(APIView):

    def get(self, request):
        print(request.query_params)

        algthm = Algorithms( request.query_params.get('type'), request.query_params.get('URL') )

        return Response(
            algthm.apriori_algorithm(
                request.query_params.get('support'),
                request.query_params.get('confidence'),
                request.query_params.get('lift')
            ),
            status=status.HTTP_200_OK
        )
