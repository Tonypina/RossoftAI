from rest_framework import serializers
from .models import Data, Report
from .algorithms import Algorithms

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = (
            'file',
        )

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = (
            'id',
            'title',
            'algorithm',
            'datetime',
            'report',
            'user'
        )