from django.contrib import admin
from django.urls import path, include

from .views import Txt2Img, my_test

urlpatterns = [
    path('txt2img/', Txt2Img.as_view(), name='txt2img'),
    path('my_test/', my_test, name='my_test'),
]
