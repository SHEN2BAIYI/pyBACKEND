from django.contrib import admin
from django.urls import path, include
from genImage import views

urlpatterns = [
    path('model-list/', views.ModelList.as_view(), name='model-list'),
    path('refresh-data/', views.RenewList.as_view(), name='refresh-data'),


]
