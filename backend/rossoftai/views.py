from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Data, Report
from .serializers import DataSerializer, ReportSerializer

class ReportListView(APIView):
    def get(self, request, *args, **kwargs):
        reports = Report.reportobjects.all()

        serializer = ReportSerializer(reports, many=True)

        return Response(serializer.data)
        