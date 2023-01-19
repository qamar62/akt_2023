from django.urls import path
from .views import hotel, check_booking, hotel_detail

urlpatterns = [
    path('', hotel , name='hotels'),
    path('hotel-detail/<uid>/' , hotel_detail , name="hotel_detail"),
    path('check_booking/' , check_booking),
    
    
    

]