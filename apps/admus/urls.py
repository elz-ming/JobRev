# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
# ========== IMPORT-ANTS ========== #

from django.urls import path
from apps.admus.views import login_user, register_user, logout_user

urlpatterns = [
    
    path('login/', login_user, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", logout_user, name="logout"),
    
]
