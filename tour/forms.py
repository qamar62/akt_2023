from django import forms
from . models import ReviewRating, TourAvailability, Tour
from datetime import date
from django.utils import timezone
from calendar import monthrange
from django.core.validators import RegexValidator
from datetime import datetime



class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']
        
class AvailabilityForm(forms.Form):
    tour = forms.ModelChoiceField(queryset=Tour.objects.all())
    month = forms.CharField(max_length=7, validators=[RegexValidator(
        r'^(19|20)\d{2}-(0[1-9]|1[0-2])$',
        message="Invalid date format. Date should be in the format YYYY-MM."
    )])

    selected_dates = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(AvailabilityForm, self).__init__(*args, **kwargs)
        self.fields['tour'].label = "Select Tour"
        self.fields['month'].label = "Select Month"
        

    def clean_month(self):
        month_str = self.cleaned_data['month']
        month_obj  = datetime.strptime(month_str, "%Y-%m")
        year = month_obj.year
        month = month_obj.month
    
        if month:
            days_in_month = monthrange(year, month)[1]
            try:
                available_dates = set(map(int, TourAvailability.objects.get(
                    tour=self.cleaned_data['tour'], month=month
                ).available_dates.split(',')))
            except ValueError:
                available_dates = set()
            try:
                unavailable_dates = set(map(int, TourAvailability.objects.get(
                tour=self.cleaned_data['tour'], month=month
            ).unavailable_dates.split(',')))
            except ValueError:
                unavailable_dates = set()
            dates = []
            for day in range(1, days_in_month + 1):
                if day in available_dates:
                    dates.append({'day': day, 'available': True})
                elif day in unavailable_dates:
                    dates.append({'day': day, 'available': False})
                else:
                    dates.append({'day': day, 'available': True})
            return {'year': month.year, 'month': month.month, 'dates': dates}
        return None
