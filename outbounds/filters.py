from django import forms
from django.db.models import fields
from django.forms import widgets
import django_filters
from . models import Otour, Tag


class OutboundFilter(django_filters.FilterSet):
    tag = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-control ',}))
    badge = django_filters.ChoiceFilter(choices=Otour.BADGE_CHOICES,widget=forms.Select(attrs={'class': 'form-control ',}))
    name = django_filters.CharFilter(widget=forms.TextInput(attrs={'class': 'form-control ',}))
      
    class Meta:
        model =  Otour
        fields = {'tag': ['exact'],'badge': ['exact'], }