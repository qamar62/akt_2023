from django.urls import path

from . import views


urlpatterns = [
    path('', views.transfer, name="transfer"),
    path('transfer-detail/', views.transferDetail, name="transfer-detail"),
    path('transfer-detail/<str:slug>/checkout/', views.tcheckout, name="transfer-checkout"),
    
    path('confirmation/', views.tConfirmation, name='t-confirmation'),
    
]

