from django.urls import path
from . import views


urlpatterns = [
    path('', views.visaDashboard, name ='visa-dashboard'),
    path('add-visa/', views.addVisa, name ='add-visa'),
    
    
    path('visa-info/', views.visaInfo, name ='visa-info'),
    path('visa-detail/', views.visaDetail, name ='visa-detail'),
]
