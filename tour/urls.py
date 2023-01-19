from django.urls import path
from . import views 

 

urlpatterns = [
    
    path('itinerary/<str:slug>/checkout/', views.checkout, name="checkout"),
    path('confirmation/', views.confirmation, name='confirmation'),
    
    #wishlist
    path('wishlist', views.wishlist, name='wishlist'),
    path('wishlist/add_to_wishlist/<int:id>', views.add_to_wishlist, name='user_twishlist'),
    
    
]
 