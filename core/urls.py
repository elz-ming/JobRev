# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include, re_path # add this
from django.conf.urls.static import static

from apps.admus.views import index, user_logout

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    re_path (r'^$', index,name='index'),
    path("", include("apps.admus.urls")), # Auth routes - login / register
    #path("", include("apps.home.urls")),
    path("logout/", user_logout, name="logout")
]