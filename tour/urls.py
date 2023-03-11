from django.urls import path
from . import views 

 

urlpatterns = [
    
    path("activity/<str:slug>/", views.tourDetail, name="tour-detail"),
    path("<int:tour_id>/<int:year>/<int:month>/", views.availability, name="tour-availability"),
    
    path("grid/", views.toursGrid, name="all-tours-grid"),
    path('itinerary/<str:slug>/checkout/', views.checkout, name="checkout"),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('initiate_payment', views.payment_view, name="payment_view"),
    # path('initiate_payment/error', views.payment_view, name="payment_view"),
    path('callback/', views.handle_callback, name='handle_callback'),
    
    
    
    #wishlist
    path('wishlist', views.wishlist, name='wishlist'),
    path('wishlist/add_to_wishlist/<int:id>', views.add_to_wishlist, name='user_twishlist'),
    path('submit_review/<int:tour_id>/' ,views.submit_review, name='submit_review'),
    
    
]
 