# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 13:10:43 2019

@author: Vishal Patel
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_filter, name='story-filter'),
    path('api/search/', views.search_api, name='story-search-api'),
    path('api/read_list', views.read_list_api, name='read-list-api'),
    path('api/crawl_test', views.update_ao3, name='crawl-test'),
]
