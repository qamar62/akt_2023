from django.urls import path
from . views import TourDetailAPIView, TourListCreateAPIView, OtourListCreateAPIView,OtourDetailAPIView

urlpatterns = [
    path('tours', TourListCreateAPIView.as_view(), name= "tour-list"),
    path('tours/<int:pk>/', TourDetailAPIView.as_view(), name= "tour-detail"),
    path('otours', OtourListCreateAPIView.as_view(), name= "otour-list"),
    path('otours/<int:pk>/', OtourDetailAPIView.as_view(), name= "otour-detail"),
]
