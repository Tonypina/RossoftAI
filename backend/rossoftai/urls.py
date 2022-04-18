from django.urls import URLPattern, path
from .views import ReportListView, UploadDataView, AprioriView

app_name = 'rossoftai'

urlpatterns = [
    path('reports/', ReportListView.as_view()),
    path('uploadData/', UploadDataView.as_view()),
    path('apriori/', AprioriView.as_view()),
]