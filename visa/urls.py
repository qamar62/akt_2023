from django.urls import path
from . import views

urlpatterns = [
    path('', views.visaInfo, name="visa-info"),
    path('visa-detail', views.visaDetail, name="visa-detail"),
]
