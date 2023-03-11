from django.db import models
from django.contrib.auth.models import User
from accounts.models import Customer
from outbounds.models import Otour
from io import BytesIO
import qrcode
from tour.models import Tour
from outbounds.models import Otour
from django.core.files import File
from PIL import Image, ImageDraw
from django.conf import settings
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.html import format_html
# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    booking_number = models.CharField(max_length=20, blank=True, null=True)
    payment_id = models.CharField(max_length=100)
    payment_method= models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.payment_id} for {self.user}'


class Booking(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Payment Pending', 'Payment Pending'),
        ('Booked', 'Booked'),
        ('Reconfirmed', 'Reconfirmed'),
        ('Cancelled', 'Cancelled'),
    )
   
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    tour = models.ForeignKey(Tour, on_delete=models.SET_NULL, blank=True, null=True)
    tour_date = models.DateField(blank=True, null=True)
    booking_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    country = models.CharField(max_length=50)
    pickup_location = models.CharField(max_length=250, blank=True)
    booking_note = models.CharField(max_length=100, blank=True)
    booking_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=50, choices=STATUS, default='Payment Pending')
    no_of_adult= models.CharField(max_length=70)
    no_of_child= models.CharField(max_length=70)
    no_of_infant= models.CharField(max_length=70)
    paymentMode = models.CharField(max_length=70)
    ip = models.CharField(blank=True, max_length=20)
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    qr_code = models.ImageField(blank=True, null=True)
    
    
   
    
    def get_absolute_url(self):
        return reverse("view-booking", args=[str(self.id)])
        
    
    
    def save(self, *args, **kwargs):
        code = qrcode.make(self.get_absolute_url)
        qr_offset = Image.new('RGB', (310, 310), 'white')
        qr_offset.paste(code)
        files_name = f'{self.booking_number}qr.png'
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.qr_code.save(files_name, File(stream), save=False)
        qr_offset.close()
        super().save(*args, **kwargs)
        
    def qr_tag(self):
        if self.qr_code != '':
            return mark_safe('<img src="%s%s" width="50" height="50" />' % (f'{settings.MEDIA_URL}', self.qr_code))

    def __str__(self):
        return self.booking_number


class Obooking(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Payment Pending', 'Payment Pending'),
        ('Booked', 'Booked'),
        ('Reconfirmed', 'Reconfirmed'),
        ('Cancelled', 'Cancelled'),
    )
   
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    otour = models.ForeignKey(Otour, on_delete=models.SET_NULL, blank=True, null=True)
    booking_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    country = models.CharField(max_length=50)
    booking_note = models.CharField(max_length=100, blank=True)
    booking_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=50, choices=STATUS, default='New')
    paymentMode = models.CharField(max_length=70)
    ip = models.CharField(blank=True, max_length=20)
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    qr_code = models.ImageField(blank=True, null=True)
    
    
    
    def save(self, *args, **kwargs):
        code = qrcode.make(self.booking_number)
        qr_offset = Image.new('RGB', (310, 310), 'white')
        qr_offset.paste(code)
        files_name = f'{self.booking_number}qr.png'
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.qr_code.save(files_name, File(stream), save=False)
        qr_offset.close()
        super().save(*args, **kwargs)
        
    def qr_tag(self):
        if self.qr_code != '':
            return mark_safe('<img src="%s%s" width="50" height="50" />' % (f'{settings.MEDIA_URL}', self.qr_code))
    
    def situation(self):
        if self.status == 'Reconfirmed':
            return format_html('<span style="color:green; font-weight:900;">{0}</span>', self.status)
        else :
            return format_html('<span style="color:#0056ae">{0}</span>', self.status)
    
    situation.allow_tags = True
    


    def __str__(self):
        return self.first_name


class BookTour(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    
    adult_quantity = models.IntegerField()
    child_quantity = models.IntegerField()
    adult_price = models.FloatField()
    child_price = models.FloatField()
    booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tour.name

class BookOtour(models.Model):
    booking = models.ForeignKey(Obooking, on_delete=models.CASCADE)
    
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    tour = models.ForeignKey(Otour, on_delete=models.CASCADE, null=True, blank=True)
    
    price = models.IntegerField()
    
    booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tour.name
    
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
