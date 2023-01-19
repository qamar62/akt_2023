
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking, Obooking
from django.conf  import settings
from django.core.mail import send_mail




# @receiver(post_save, sender = Obooking)
# def send_email_after_booking(sender, instance,created, **kwargs):
#     if created:
#         booking_number = instance.booking_number
#         subject = instance.booking_number
#         email = instance.email
#         name = instance.first_name
#         phone = instance.phone
#         timestamp = instance.created_at
#         total_price = instance.booking_total
        
#         from_email = settings.EMAIL_HOST_USER
#         message = f"{booking_number} has been received from {name} with phone {phone} on {timestamp} total price {total_price}"

#         recipient_list = [email]
#         send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
#         print("email sent")
