from django import forms
from .models import Booking, Obooking, TransferBooking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['first_name', 'last_name', 'phone','email', 'pickup_location', 'country', 'booking_note','paymentMode']


class ObookingForm(forms.ModelForm):
    class Meta:
        model = Obooking
        fields = ['first_name', 'last_name', 'phone','email', 'country', 'booking_note','paymentMode']


class TransferForm(forms.ModelForm):
    class Meta:
        model = TransferBooking
        fields = ['fullname', 'phone','email', 'service_date', 'service_time','pickup_location','dropoff_location']