# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.dashboard.views import index, dashboard, pages 

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name="dashboard"),
    re_path(r'^.*\.*', pages, name='pages'),
]
