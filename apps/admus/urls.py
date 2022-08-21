# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.admus.views import login_view, register_user, pages, index, user_logout

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", user_logout, name="logout"),
    re_path(r'^.*\.*', pages, name='pages'),
]
