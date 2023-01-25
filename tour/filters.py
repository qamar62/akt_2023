import django_filters
from django_filters import DateFilter, CharFilter

from tour.models import *

class TourCatFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name="date_created", lookup_expr='gte')
    # end_date =  DateFilter(field_name="date_created", lookup_expr='lte')
    # pickup = CharFilter(field_name="pickup", lookup_expr='icontains')
    
    class Meta:
        model = Tour
        fields =  ['category']
        