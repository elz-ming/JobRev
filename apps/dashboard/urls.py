# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.dashboard.views import index, dashboard1, dashboard2, pages 

urlpatterns = [
    path('', index, name='index'),
    path('dashboard1/', dashboard1, name="dashboard1"),
    path('dashboard2/', dashboard2, name="dashboard2"),
    re_path(r'^.*\.*', pages, name='pages'),
]
