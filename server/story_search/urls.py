# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 13:10:43 2019

@author: Vishal Patel
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_filter, name='story-filter'),
    path('api/', views.api, name='story-search-api')
]
