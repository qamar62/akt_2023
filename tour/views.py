from http.client import HTTPResponse
from django.shortcuts import render, redirect, get_object_or_404
import datetime
import time

from . filters import TourCatFilter
from . models import Tour, TourService, TourGallery, ReviewRating
from . forms import ReviewForm
# Create your views here.


from django.http import HttpResponse, HttpResponseRedirect
from bookings.forms import BookingForm
from bookings.models import  Booking
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from bookings.twilio import client
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator



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
    
    current_user = request.user
    tax = 0
    grand_total = 0
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
            message.send()
            client.messages.create(
                     body=f"Thank you for bchoosing Arabian Nights Tours , Your booking number is {booking_number}",
                     from_='+14793481542',
                     to=data.phone,
                 )
            
            
            
            
            
            context = {
                'booking' : booking,
                'total': total,
                'tax' : tax,
                'grand_total' : grand_total,
                
            }
                
                

            return render(request, 'tour/confirmation.html', context)

        else:
            return HttpResponse('Booking not saved')
                           
    
    
    context = {'tour':tour}
    return render (request, 'tour/tbookingForm.html', context)


def confirmation(request):
    
    context = {}
    return redirect(request, 'tour/confirmation.html', context)




def tourDetail(request, slug):

    tour_service = TourService.objects.all()
    tour = Tour.objects.get(slug=slug)
    for price in tour.price.all() :
        adult_price = price.adult_price 
        child_price = price.child_price 
        infant_price = price.infant_price 
   
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        print(quantity)        
    
    
    tour_gallery = TourGallery.objects.all()
    reviews = ReviewRating.objects.all()
    
    context = {'tour':tour, 'tour_service':tour_service, 'tour_gallery':tour_gallery, "reviews":reviews, "adult_price":adult_price, "child_price":child_price }
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


    context = {'tours': paged_tours,  'tour_count':tour_count, 'catfilter':catfilter, 'all_tours':tours}
    return render( request, "tour/all_tours_grid.html", context )

