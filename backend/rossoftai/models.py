
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

def user_directory_report_path(instance, filename):
    return 'rossoftai/reports/{0}/{1}/{2}'.format(instance.algorithm, instance.algorithm, filename)

def user_directory_data_path(instance, filename):
    return 'rossoftai/data/{0}/{1}'.format(instance.algorithm, filename)

class Data(models.Model):

    class DataObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset()

    data_source = models.FileField(upload_to=user_directory_data_path, null=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='data_user')

    objects = models.Manager()
    dataobjects = DataObjects()
    

class Report(models.Model):

    class ReportObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset()

    options = (
        ('apriori', 'Apriori' ),
        ('metrics', 'Metrics' ),
        ('clusteringH', 'ClusteringH' ),
        ('clusteringP', 'ClusteringP' ),
    )

    title = models.CharField(max_length=250)
    algorithm = models.CharField(max_length=12, choices=options)
    datetime = models.DateTimeField(default=timezone.now)
    report = models.FileField(upload_to=user_directory_report_path, null=False)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_user')

    objects = models.Manager()
    reportobjects = ReportObjects()

    class Meta:
        ordering = ('-datetime')

    def __str__(self):
        return self.title