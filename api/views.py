from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import mixins
from outbounds.models import Otour
from tour.models import Tour
from .serializer import OtourSerializer, TourSerializer

from rest_framework.permissions import IsAuthenticated
from .permissions import isAdminUserReadOnly
from .pagination import SmallSetPagination


# Create your views here.

class TourListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [isAdminUserReadOnly, IsAuthenticated]

class TourDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [isAdminUserReadOnly, IsAuthenticated]


class OtourListCreateAPIView(generics.ListCreateAPIView):
    queryset = Otour.objects.all()
    serializer_class = OtourSerializer
    permission_classes = [isAdminUserReadOnly, IsAuthenticated]
    pagination_class = SmallSetPagination

class OtourDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Otour.objects.all()
    serializer_class = OtourSerializer
    permission_classes = [isAdminUserReadOnly, IsAuthenticated]


# @api_view(['GET'])
# def tourList(request):
#     tours = Tour.objects.all()
#     serializer = TourSerializer(tours, many=True)
#     return Response(serializer.data)
