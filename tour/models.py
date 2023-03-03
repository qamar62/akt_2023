from django.db import models
from django.template.defaultfilters import slugify

from django.db.models import Avg, Count
from django.urls import reverse
from accounts.models import Customer
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from calendar import monthrange

# Create your models here.



class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)
    
    def __unicode__(self):
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

class Tour(models.Model):
    
    name = models.CharField(max_length=200)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
   
    duration = models.IntegerField(default=0)
    description = RichTextField(help_text='Description of tour', blank=True, null=True)
    shortdesc = models.CharField(max_length=200)
    groupsize = models.IntegerField(default=0)
    highlights = models.CharField(max_length=100)
    thumbnail = models.ImageField(null=True, blank=True)
    
    rating = models.IntegerField()
    starttime = models.TimeField()
    endtime =  models.TimeField()
    tag = models.ManyToManyField(Tag)
    
       
    slug = models.SlugField(max_length=150, default='null', unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    badge = models.CharField(max_length=200, choices=(('Popular', 'Popular'),('Top Rated', 'Top Rated'),))
    user_wishlist = models.ManyToManyField(User, related_name='user_twishlist', blank=True)
    
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    
    def get_absolute_url(self):
        return reverse("tour-detail", kwargs={"slug": self.slug})

class Price(models.Model):
    SERVICE_CHOICE = (('Private', 'Private'), ('Sharing', 'Sharing'))
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="price")
    service_type = models.TextField(choices=SERVICE_CHOICE, max_length=100, null=True, blank=True)
    base_Price = models.FloatField()
    adult_price = models.FloatField()
    child_price = models.FloatField()
    infant_price = models.FloatField()
      
    
    
    def __str__(self):
        return f'{self.tour.name} - {self.service_type}'

class TourAvailability(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    month = models.DateField()
    available_dates = models.CharField(max_length=100, blank=True, help_text="system will assign automatically")
    unavailable_dates = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        days_in_month = monthrange(self.month.year, self.month.month)[1]
        all_dates = set(range(1, days_in_month+1))
        unavailable_dates = set(map(int, str(self.unavailable_dates).split(','))) if self.unavailable_dates is not None else set()
        available_dates = sorted(list(all_dates - unavailable_dates))
        self.available_dates = ",".join([str(day) for day in available_dates])
        super(TourAvailability, self).save(*args, **kwargs)
        
        

class Extra(models.Model):
    
    title = models.CharField(max_length= 200 , blank=True, null=True)
    price = models.IntegerField()
    icon = models.ImageField(null=True, blank=True)
    available = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    

class TourGallery(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='gallery')
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
  
   tour = models.ForeignKey(Tour, related_name="itinerary", on_delete=models.CASCADE)
   title = models.CharField(max_length= 200 , blank=True, null=True)
   time = models.CharField(max_length= 200 , blank=True, null=True)
   icon = models.ImageField(null=True, blank=True)
   detail = models.TextField(null=True, blank=True)
   
   def __unicode__(self):
            return f'{self.title} - {self.tour.name} '
   class Meta: 
        verbose_name = "Itinerary"
        verbose_name_plural = "Itineraries"

class Excl(models.Model):
    
    tour  = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='excludes')
    body   = RichTextField(blank=True, null=True)
    icon = models.ImageField(null=True, blank=True)
   
    

    def __str__(self):
        return  self.tour.name


class Inclusions(models.Model):
    tour  = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='includes')
    body   = RichTextField(blank=True, null=True)
    icon = models.ImageField(null=True, blank=True)

    
    def __str__(self):
        return  self.tour.name
    
    class Meta: 
        verbose_name = "Inclusion"
        verbose_name_plural = "Inclusions"  


class Promotion(models.Model):
    
    tour = models.OneToOneField('Tour', on_delete=models.CASCADE)
    percentage = models.PositiveSmallIntegerField(choices=[(x, x) for x in range(5, 101, 5)])
    begin_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.tour}: {self.percentage}% - {self.begin_date} to {self.end_date}"


class ReviewRating(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject