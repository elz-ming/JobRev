# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
# ========== IMPORT-ANTS ========== #

from django.apps import AppConfig


class AdmusConfig(AppConfig):
    name = 'apps.admus'
    label = 'apps_admus'
    
    def ready(self):
        from apps.jsscraper import updater
        updater.start()
