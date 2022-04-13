from django.urls import URLPattern, path
from .views import ReportListView

app_name = 'rossoftai'

urlpatterns = [
    path('reports/', ReportListView.as_view())
]