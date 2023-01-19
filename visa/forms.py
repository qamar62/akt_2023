from dataclasses import fields
from django import forms
from django.forms import ModelForm
from. models import Visa

class VisaForm(forms.ModelForm):

    class Meta:
        model = Visa
        fields = '__all__'

        widgets = {
            'agent' : forms.Select(attrs={'class': 'form-control'}),
            'guest_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'guest_passport_number' : forms.TextInput(attrs={'class': 'form-control'}),
            'guest_nationality' : forms.TextInput(attrs={'class': 'form-control'}),
            'guest_gender' : forms.TextInput(attrs={'class': 'form-control'}),
            'visa_status' : forms.Select(attrs={'class': 'form-control'}),
            'visa_type' : forms.Select(attrs={'class': 'form-control'}),
            'visa_price' : forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            
        }