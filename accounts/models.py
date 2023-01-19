from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField
from datetime import datetime
from django.template.defaultfilters import slugify




# Create your models here.


    
    

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True,  on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    email_token =  models.CharField(max_length=200, blank=True)
    is_varified = models.BooleanField(default=False, null=True)
    profile_pic = models.ImageField(null = True, blank = True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


    
class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=30,blank=True, null=True)
    email = models.EmailField(max_length=100)
    message = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True, blank=True)


    def __str__(self):
        return f"{self.name} has phone number {self.phone}"