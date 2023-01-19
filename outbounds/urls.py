from django.urls import path
from . import views


urlpatterns = [
    path('', views.outbounds, name="outbounds"),
    path('list-view', views.outboundListview, name="list-view"),
    path('itinerary/<str:slug>/', views.outbound_detail, name="outbound-detail"),
    path('itinerary/<str:slug>/checkout/', views.ocheckout, name="ocheckout"),
    path('create-booking/', views.createObooking, name="create-booking"),
   
    
    path('confirmation/', views.Oconfirmation, name='Oconfirmation'),
    path('invoice/', views.Oinvoice, name='o_invoice'),
    
    #wishlist
    path('wishlist', views.wishlist, name='wishlist'),
    path('wishlist/add_to_wishlist/<int:id>', views.add_to_wishlist, name='user_wishlist'),
]
