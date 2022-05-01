from django.urls import URLPattern, path
from .views import ReportListView, AlgorithmView

app_name = 'rossoftai'

urlpatterns = [
    path('reports/', ReportListView.as_view()),
    path('runAlgorithm/', AlgorithmView.as_view())
]