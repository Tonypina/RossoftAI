from django.contrib import admin
from .models import Data, Report

admin.site.register([Data, Report])