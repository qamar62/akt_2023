from platform import release
from django.db import models
from django.template.defaultfilters import slugify

from django.db.models import Avg, Count
from django.urls import reverse
from accounts.models import Customer
from auditlog.registry import auditlog
from ckeditor.fields import RichTextField
# Create your models here.

from django.contrib.auth.models import User



class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    cat_icon =  models.ImageField(null=True, blank=True)
    created_on =  models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name =  'category'
        verbose_name_plural = 'catagories'

    def __str__(self):
        return self.name



class Location(models.Model):
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=150, null=True, blank=True)


    def __str__(self):
        return self.city

class Otour(models.Model):
    
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    no_of_days = models.IntegerField(default=0)
    no_of_nights = models.IntegerField(default=0)
    description = RichTextField(help_text='Description of tour', blank=True, null=True)
    highlights = models.CharField(max_length=100)
    thumbnail = models.ImageField(null=True, blank=True)
    departure_date = models.DateField()
    tag = models.ManyToManyField(Tag)
    slug = models.SlugField(max_length=150, default='null', unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    badge = models.CharField(max_length=200, choices=(('Popular', 'Popular'),('Top Rated', 'Top Rated'),))
    seats = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    user_wishlist = models.ManyToManyField(User, related_name='user_wishlist', blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("outbound-detail", args=[str(self.slug)])
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("outbound-detail", kwargs={"slug": self.slug})
    
    class Meta:
        verbose_name =  'Outbound Tour'
        verbose_name_plural = 'Outbound Tours'
        ordering = ['-date_created']
    
    
class Price(models.Model):
      tour = models.ForeignKey(Otour, on_delete=models.CASCADE, related_name="price")
      guest = models.CharField(max_length=200)
      price = models.IntegerField(default=0)
      

class Optional(models.Model):
    tour = models.ForeignKey(Otour, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    adult_price = models.CharField(max_length=200, help_text="18+")
    single_price = models.CharField(max_length=200)
    Child1_price = models.CharField(max_length=200, help_text="2-5 Years")
    Child2_price = models.CharField(max_length=200, help_text="6-11 Years")
    infant_price = models.CharField(max_length=200, help_text="1-2 Years")
    
    
       


    

class OtourGallery(models.Model):
    tour = models.ForeignKey(Otour, on_delete=models.CASCADE, related_name='ogallery')
    image1 = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    image4 = models.ImageField(null=True, blank=True)
    image5 = models.ImageField(null=True, blank=True)
    image6 = models.ImageField(null=True, blank=True)


    def __str__(self):
        return f' {self.tour.name}  - image gallery '
    class Meta: 
        verbose_name = "Gallery"
        verbose_name_plural = "Galleries"

class Itinerary(models.Model):
  
   tour = models.ForeignKey(Otour, related_name="itinerary", on_delete=models.CASCADE)
   title = models.CharField(max_length= 200 , blank=True, null=True)
   time = models.CharField(max_length= 200 , blank=True, null=True)
   icon = models.ImageField(null=True, blank=True)
   detail = models.TextField(null=True, blank=True)
   
   def __unicode__(self):
            return f'{self.title} - {self.tour.name} '
   class Meta: 
        verbose_name = "Itinerary"
        verbose_name_plural = "Itineraries"

class Exclusions(models.Model):
    
    tour  = models.ForeignKey(Otour, on_delete=models.CASCADE, related_name="excludes")
    name = models.CharField(max_length=250)
    icon = models.ImageField(null=True, blank=True)
   
    

    def __str__(self):
        return  self.tour.name


class Inclusions(models.Model):
    tour  = models.ForeignKey(Otour, on_delete=models.CASCADE, related_name="includes")
    name = models.CharField(max_length=250)
    icon = models.ImageField(null=True, blank=True)

    
    def __str__(self):
        return  self.tour.name
    
    class Meta: 
        verbose_name = "Inclusion"
        verbose_name_plural = "Inclusions"




class Offer(models.Model):
    
    tour = models.OneToOneField('Otour', on_delete=models.CASCADE)
    percentage = models.PositiveSmallIntegerField(choices=[(x, x) for x in range(5, 101, 5)])
    begin_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.tour}: {self.percentage}% - {self.begin_date} to {self.end_date}"



auditlog.register(Otour)