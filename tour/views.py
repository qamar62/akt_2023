import calendar
from http.client import HTTPResponse
from django.shortcuts import render, redirect, get_object_or_404
import datetime
import time
from django.views.decorators.csrf import csrf_exempt
import requests
from . filters import TourCatFilter
from . models import Tour, TourAvailability, TourGallery, ReviewRating
from . forms import  AvailabilityForm, ReviewForm
# Create your views here.

import xml.etree.ElementTree as ET
import xmltodict
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from bookings.forms import BookingForm
from bookings.models import  Booking, Payment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from bookings.twilio import client
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

import json






@login_required
def wishlist(request):
    tours = Tour.objects.filter(user_wishlist=request.user)
    
    
    context = {'wishlist':tours}
    return render(request, 'tour/wishlist.html', context)

@login_required
def add_to_wishlist(request, id):
    tour = get_object_or_404(Tour, id=id)
    if tour.user_wishlist.filter(id=request.user.id).exists():
        tour.user_wishlist.remove(request.user)
        time.sleep(3)
        messages.success(request,  tour.name + " has been removed from your Wishlist")
    else:
        tour.user_wishlist.add(request.user)
        time.sleep(3)
        messages.success(request, "Added " + tour.name + " to your Wishlist")
        
    return HttpResponseRedirect(request.META["HTTP_REFERER"])



@login_required
def checkout(request, slug):
    
    
    tour = Tour.objects.get(slug=slug)
    
    current_user = request.user.customer
    tax = 0
    grand_total = 150
    total = 0
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():

            data = Booking()
            data.user =  current_user
            data.first_name = form.cleaned_data["first_name"]
            data.last_name = form.cleaned_data["last_name"]
            data.phone = form.cleaned_data["phone"]
            data.email = form.cleaned_data["email"]
            
            data.country = form.cleaned_data["country"]
            data.pickup_location = form.cleaned_data["pickup_location"]
            data.booking_note = form.cleaned_data["booking_note"]
            data.paymentMode = form.cleaned_data["paymentMode"]
            data.tour_date = form.cleaned_data["tour_date"]
            if data.tour_date:
                data.tour_date = datetime.strptime(data.tour_date, '%d-%m-%Y').date()
            else:
                data.tour_date = None
            data.booking_total = grand_total
            data.tax  = tax
            data.tour= tour
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # generate booking number 
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            booking_number = current_date + str(data.id)
            data.booking_number = booking_number
            data.save()
            
            booking = Booking.objects.get(user=current_user, is_booked=False, booking_number = booking_number)
            
            # after Booking done send email to Customer
            html_template = 'tour/booking_email.html'
            subject = 'Thank you for your Booking!'
            html_message = render_to_string(html_template, {
                'user': request.user,
                'booking_number': booking_number,
                'booked_date': data.created_at,
                'payment_method':data.paymentMode,
                'total':data.booking_total,
            })
            recipient_list = [data.email]
            email_from = settings.EMAIL_HOST_USER
            message = EmailMessage(subject, html_message, email_from, recipient_list)
            message.content_subtype = "html"
            # message.send()
            # client.messages.create(
            #          body=f"Thank you for bchoosing Arabian Nights Tours , Your booking number is {booking_number}",
            #          from_='+14793481542',
            #          to=data.phone,
            #      )
            
            
            
            
            
            context = {
                'booking' : booking,
                'total': total,
                'tax' : tax,
                'grand_total' : grand_total,
                
            }
                
                

            return render(request, 'tour/booking-confirmation.html', context)

        else:
            return HttpResponse('Booking not saved')
                           
    
    
    context = {'tour':tour}
    return render (request, 'tour/tbookingForm.html', context)

def payment_view(request):
    current_user = request.user.customer
    bookings = Booking.objects.filter(user=current_user, is_booked=False)
    for booking in bookings:
        booking_number = booking.booking_number
        customer_name = request.user.customer.name
        customer_email = request.user.customer.email
        service_name = booking.tour.name
        amount = booking.booking_total
    # 3G Direct Pay API endpoint
    url = 'https://secure.3gdirectpay.com/API/v6/'

    # XML request to create token for payment
    xml = '''<?xml version="1.0" encoding="utf-8"?>
    <API3G>
    <CompanyToken>8D3DA73D-9D7F-4E09-96D4-3D44E7A83EA3</CompanyToken>
    <Request>createToken</Request>
    <Transaction>
    <PaymentAmount>0</PaymentAmount>
    <PaymentCurrency>AED</PaymentCurrency>
    <CompanyRef>DNPEPU</CompanyRef>
    <RedirectURL>https://arabianknightstours.com/callback/</RedirectURL>
    <BackURL></BackURL>
    <CompanyRefUnique>0</CompanyRefUnique>
    <PTL>1</PTL>
    </Transaction>
    <Services>
    <Service>
    <ServiceType>5525</ServiceType>
    <ServiceDescription>Desert Safari</ServiceDescription>
    <ServiceDate>2013/12/20 19:00</ServiceDate>
    </Service>
    </Services>
    </API3G>'''
    
    
    # parse the XML string
    root = ET.fromstring(xml)

    # find the PaymentAmount element and update its value
    payment_amount = root.find('Transaction/PaymentAmount')
    payment_amount.text = str(amount)  # set the new value here
    
    serviceDescription = root.find('Services/Service/ServiceDescription')
    serviceDescription.text = service_name
    # serialize the updated XML
    updated_xml = ET.tostring(root).decode('utf-8')
    
    print(updated_xml)
   
    
    # Headers for the XML request
    headers = {'Content-Type': 'application/xml'}

    # Send the XML request to the 3G Direct Pay API endpoint
    response = requests.post(url, data=updated_xml, headers=headers)
    
    # Parse the response from the API
    response_xml = response.content.decode('utf-8')
    print(response_xml)
    response_dict = xmltodict.parse(response_xml.encode('utf-8'))
    
    
    

    # Check if the payment request was successful
    if response_dict['API3G']['Result'] == '000':
        # Get the payment URL
        TransToken = response_dict['API3G']['TransToken']
        transaction_id = response_dict['API3G']['TransRef']
        print(transaction_id)
        
        
        print(TransToken)
        # Redirect to the payment URL
        payment_url = f'https://secure.3gdirectpay.com/payv2.php?ID={TransToken}'
        
        # Create a new payment object and save it to the database
        payment = Payment(
            booking_number=booking_number,
            user=request.user.customer,
            
            amount=amount,
            payment_id=transaction_id,
            status='pending',
        )
        payment.save()
        
        return redirect(payment_url)
    else:
        # Payment request was not successful, handle the error
        error_message = response_dict['API3G']['ResultExplanation']
        return HttpResponse(error_message)
   
@csrf_exempt 
def handle_callback(request):
    if request.method == 'POST':
        # Parse the callback data and extract the transaction ID and status
        callback_data = json.loads(request.body.decode('utf-8'))
        transaction_id = callback_data['TransactionID']
        status = callback_data['Status']

        # Find the corresponding payment in the database
        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
        except Payment.DoesNotExist:
            return JsonResponse({'error': 'Payment not found'}, status=404)

        # Update the payment status based on the callback data
        payment.status = status
        payment.save()
        current_user = request.user.customer
        booking = Booking.objects.get(user=current_user, is_booked=False)
        if booking:
            # Update the booking status to "Paid"
            booking.status = "Booked"
            booking.is_booked = True
            booking.save()

        # Return a success response
        return HttpResponse('Callback handled successfully')
    else:
        # Handle invalid requests
        return HttpResponseBadRequest()
    

def confirmation(request):
    
    context = {}
    return redirect(request, 'tour/booking-paid-confirmation.html', context)




def tourDetail(request, slug):
    top_tours = Tour.objects.filter(available=True)[:4]
    
    tour = Tour.objects.get(slug=slug)
    private_tour_price = None
    sharing_tour_price = None
    for price in tour.price.all():
        if price.service_type == 'Private':
            private_tour_price = price
        else:
            sharing_tour_price =  price
   
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        print(quantity)        
    
    
    tour_gallery = TourGallery.objects.all()
    reviews = ReviewRating.objects.all()
    
    context = {'tour':tour, 'tour_gallery':tour_gallery, "reviews":reviews, "private_tour_price":private_tour_price, "sharing_tour_price":sharing_tour_price , "top_tours":top_tours}
    return render( request, "tour/tourdetails.html", context )



def submit_review(request, tour_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, tour__id=tour_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.tour_id = tour_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)

def toursGrid(request):
    tours = Tour.objects.all()
    paginator = Paginator(Tour.objects.all(), 3)
    page =  request.GET.get('page')
    paged_tours =  paginator.get_page(page)
    tour_count =  tours.count()

    catfilter =  TourCatFilter()
    private_tour_price = None
    sharing_tour_price = None
    for tour in tours:
        for price in tour.price.all():
            if price.service_type == 'Private':
                private_tour_price = price
            else:
                sharing_tour_price =  price

    context = {'tours': paged_tours,  'tour_count':tour_count, 'catfilter':catfilter, 'all_tours':tours, "private_tour_price":private_tour_price, "sharing_tour_price":sharing_tour_price,}
    return render( request, "tour/all_tours_grid.html", context )




def tour_availability(request, tour_id, year=2023, month=3):
    tour_availability = TourAvailability.objects.get(tour_id=tour_id, month__year=year, month__month=month)
    context = {
        'tour_availability': tour_availability
    }
    return render(request, 'tour/tour_availability.html', context)




def availability(request, tour_id, year, month):
    
    tour_availability = TourAvailability.objects.filter(tour_id=tour_id, month__year=year, month__month=month)
    
    context = {'tour_availability': tour_availability}
    return render(request, 'tour/availability.html', context)
