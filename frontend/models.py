from unittest.util import _MAX_LENGTH
from django.db import models



class Newsletter(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.email
 
 
 
class FaqServices(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    
class Faq(models.Model):
    service = models.ForeignKey(FaqServices, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=300)
    answer = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.question
    

class HappyCutomer(models.Model):
    customer_name = models.CharField(max_length=50)
    image = models.ImageField()
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    
    
    def __str__(self):
        return self.customer_name
    
    
    