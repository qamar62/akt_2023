import random
from django.db import models

# Create your models here.


class B2bAgent(models.Model):
    agent_code = models.CharField(max_length=25, unique=True, blank=True)
    agent_credit_limit = models.IntegerField()
    agent_name = models.CharField(max_length=100)
    agent_company_name = models.CharField(max_length=100)
    agent_username = models.CharField(max_length=100)
    agent_email = models.CharField(max_length=100)
    agent_mobile = models.CharField(max_length=100)
    agent_desination = models.CharField(max_length=100)
    agent_city = models.CharField(max_length=100)
    agent_country = models.CharField(max_length=100)
    agent_currency = models.CharField(max_length=100, choices=(('AED', 'AED'), ('INR', 'INR'), ('PKR', 'PKR'),('IDR', 'IDR')))
    agent_TRN  = models.CharField(max_length=100, help_text="Tax Registered Number")
    is_active = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    
    def save(self,  *args, **kwargs):
        code = str(random.randint(1000, 5000))
        prefix = "ANT"
        self.agent_code = prefix+code
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.agent_company_name
    
  