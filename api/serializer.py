from rest_framework import serializers
from outbounds.models import Otour
from tour.models import Tour


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        
        exclude = ['date_created', 'date_updated']

class OtourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otour
        
        exclude = ['date_created', 'date_updated']

