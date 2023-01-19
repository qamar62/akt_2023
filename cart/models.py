from django.db import models
from django.contrib.auth.models import User
from outbounds.models import Otour
from tour.models import Tour, Extra


# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)



    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, null=True, related_name="tour_cartitems")
    
    otour = models.ForeignKey(Otour, on_delete=models.CASCADE, null=True, related_name="otour_cartitems")
    
    
    # variations =  models.ManyToManyField(Variation, blank=True)
    cart  = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    adult_quantity = models.IntegerField()
    child_quantity = models.IntegerField()
    
    
    
    is_active = models.BooleanField(default=True)

    
    
    
    


    def __str__(self):
        return self.tour


