from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

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

        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AprioriView(APIView):

    def get(self, request):
        print(request.query_params)

        # return Response(request.query_params, status=status.HTTP_200_OK)

        algthm = Algorithms( request.query_params.get('type'), request.query_params.get('URL') )

        return Response(
            algthm.apriori_algorithm(
                request.query_params.get('support'),
                request.query_params.get('confidence'),
                request.query_params.get('lift')
            ),
            status=status.HTTP_200_OK
        )
