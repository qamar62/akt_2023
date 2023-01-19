from django.urls import path
from . import views

urlpatterns = [
    path('create_booking/', views.create_booking, name='create_booking'),
    
    path('payments/', views.payments, name='payments'),
    path('thankyou/', views.booking_complete, name='booking_complete'),
    
    path('view-booking/<int:id>', views.viewBooking, name='view-booking'),
    path('view-tbooking/<int:id>', views.viewTourBooking, name='view-tbooking'),
    
    path('invoice/', views.invoice, name='invoice'),


    # path('update_booking/<str:pk>/', views.updateBooking, name = 'update_booking'),
    # path('delete_booking/<str:pk>/', views.deleteBooking, name = 'delete_booking'),
]
