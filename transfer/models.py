from django.db import models
from django.template.defaultfilters import slugify

from accounts.models import Customer

# Create your models here.


class PickupLocation(models.Model):
    location = models.CharField(max_length=200)
    def __str__(self):
        return self.location
    
class DropoffLocation(models.Model):
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.location
    


class Transfer(models.Model):
    
    name = models.CharField(max_length=200)
    
    description = models.TextField(help_text='Description of tour')
    max_seats = models.CharField(max_length=200)
    display_image = models.ImageField(null=True, blank=True)
    slug = models.SlugField(max_length=150, default='null', unique=True)
    transfer_type = models.CharField(max_length=20, choices=(('Sharing' , 'sharing'),  ('Private' , 'Private')), blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    available = models.BooleanField(default=True)
    
    
    
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
        
class Price(models.Model):
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE, related_name='price')
    oneway_price = models.CharField(max_length=50, null=True, blank=True)
    return_price = models.CharField(max_length=50, null=True, blank=True)
    
    
    
class TransferBooking(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Payment Pending', 'Payment Pending'),
        ('Booked', 'Booked'),
        ('Reconfirmed', 'Reconfirmed'),
        ('Cancelled', 'Cancelled'),
    )
   
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    
    booking_number = models.CharField(max_length=20)
    fullname = models.CharField(max_length=50)
    service_date = models.DateField(null=True, blank=True)
    service_time = models.TimeField(null=True, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    pickup_location = models.CharField(max_length=50)
    dropoff_location = models.CharField(max_length=100, blank=True)
    booking_total = models.FloatField(null=True, blank=True)
    tax = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS, default='New')
    paymentMode = models.CharField(max_length=70,null=True, blank=True)
    ip = models.CharField(blank=True, max_length=20)
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    


    def __str__(self):
        return self.first_name
