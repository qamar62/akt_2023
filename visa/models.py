from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Agent(models.Model):
    name = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE )
    agent_code = models.CharField(max_length=20, null=True, blank=True)
    
    
    def __str__(self):
        return self.agent_code

  
 
class VisaType(models.Model):
    
    title = models.CharField(max_length=200, blank=True, null=True)
    validity = models.IntegerField()
    multiple_entry = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    
    
    def __str__(self):
        return self.title
    
class VisaPrice(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    visa_type = models.ManyToManyField(VisaType)
    price = models.IntegerField()
    currency = models.CharField(max_length=3,  choices=(('PKR', 'PKR'), ('AED', 'AED')), null=True, blank=True, default='PKR')
    
    
    def __str__(self):
        return f'{self.price}{self.currency}'
    
class Visa(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name= "visa")
    VISASTATUS = [
        ('INPROCESS', 'INPROCESS'),
        ('APPROVED', 'APPROVED'),
        ('REJECTED', 'REJECTED')
    ]
    guest_name = models.CharField(max_length=50, blank=True, null=True)
    guest_passport_number = models.CharField(max_length=25, blank=True, null=True)
    guest_nationality = models.CharField(max_length=50, blank=True, null=True)
    guest_gender = models.CharField(max_length=50, blank=True, null=True)
    visa_status = models.CharField(max_length=10,  choices=VISASTATUS, default="INPROCESS")
    visa_type = models.ForeignKey(VisaType, on_delete=models.CASCADE, blank=True, null=True, related_name='visatype' )
    visa_price = models.ForeignKey(VisaPrice, on_delete=models.CASCADE, blank=True, null=True, related_name='visaprice')

    class Meta:
        ordering = ['-id']
    
    
    def __str__(self):
        return self.guest_name
     
    
