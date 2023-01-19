from email import message
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Customer
from django.conf  import settings
from django.core.mail import send_mail
import uuid






def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        uid = uuid.uuid4()
        Customer.objects.create(
            user = instance,
            name = instance.username,
            email = instance.email,
            email_token = uid,
            
            )
            
post_save.connect(customer_profile, sender = User)


def send_email_after_registration(sender, instance,created, **kwargs):
    if created:
        subject = 'Varify Email'
        email = instance.email
        token =  instance.email_token
        from_email = settings.EMAIL_HOST_USER
        message = f'Hi Click on the link to varify your account http://arabiannights.tours/accounts/account-verify/{token}'
        recipient_list = [email]
        send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
        
post_save.connect(send_email_after_registration, sender = Customer)

        
