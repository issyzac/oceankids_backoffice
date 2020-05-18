# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    path('kid-details/<str:child_id>/', views.kid_details),

    # Matches any html file 
    re_path(r'^.*', views.pages, name='pages'),

    # The home page
    path('', views.index, name='home'),
]
