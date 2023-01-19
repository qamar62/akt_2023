from django.db import models
from django.template.defaultfilters import slugify

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