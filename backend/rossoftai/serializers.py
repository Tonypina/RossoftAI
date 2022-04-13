from dataclasses import field
from rest_framework import serializers
from .models import Data, Report

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = (
            'id',
            'data_source',
            'user'
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
