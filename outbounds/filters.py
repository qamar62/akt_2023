from django import forms
from django.db.models import fields
from django.forms import widgets
import django_filters
from . models import Otour


class OutboundFilter(django_filters.FilterSet):
    
   
    
    class Meta:
        model =  Otour
        fields = {'tag': ['exact'],'badge': ['exact'],'name': ['icontains'], }
        
       