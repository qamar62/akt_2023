from django import forms
from .models import Booking, Obooking

from django.forms.widgets import DateInput

class BookingForm(forms.ModelForm):
    tour_date = forms.DateField(input_formats=['%d-%m-%Y'], widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    class Meta:
        model = Booking
        fields = ['first_name', 'last_name', 'phone','email', 'pickup_location', 'country', 'booking_note','paymentMode', 'tour_date']
        

class ObookingForm(forms.ModelForm):
    class Meta:
        model = Obooking
        fields = ['first_name', 'last_name', 'phone','email', 'country', 'booking_note','paymentMode']


