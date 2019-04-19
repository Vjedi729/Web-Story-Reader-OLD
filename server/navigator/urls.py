# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 13:04:16 2019

@author: Vishal Patel
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='navigator-home'),
    path('about/', views.about, name='navigator-about'),
    #path('register/', views.register, name='register'),
    #path('login/', views.login, name='login'),
]
