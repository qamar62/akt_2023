from http.client import HTTPResponse
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from cart.models import Cart, CartItem
from . models import Itinerary, Otour, Price
# Create your views here.
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .filters import OutboundFilter
from django.http import HttpResponse, HttpResponseRedirect
from bookings.forms import ObookingForm
from bookings.models import  BookOtour, Obooking
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings



@login_required
def wishlist(request):
    otours = Otour.objects.filter(user_wishlist=request.user)
    
    
    context = {'wishlist':otours}
    return render(request, 'outbounds/wishlist.html', context)


@login_required
def add_to_wishlist(request, id):
    otour = get_object_or_404(Otour, id=id)
    if otour.user_wishlist.filter(id=request.user.id).exists():
        otour.user_wishlist.remove(request.user)
        messages.success(request,  otour.name + " has been removed from your Wishlist")
    else:
        otour.user_wishlist.add(request.user)
        messages.success(request, "Added " + otour.name + " to your Wishlist")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

def outbounds(request):
    
    outbounds_tours = Otour.objects.all()
    outbounds_filter = OutboundFilter(request.GET, queryset=outbounds_tours)
    prices = Price.objects.all()
    paginator = Paginator(outbounds_filter.qs, 6)
    page =  request.GET.get('page', 1)
    paged_tours =  paginator.get_page(page)
        
            
    
    context = {'outbounds_filter':paged_tours, 'prices':prices, 'outbounds':outbounds_tours}
    return render(request, 'outbounds/outbounds.html', context)


def outbound_detail(request, slug):
    
    
    otour = Otour.objects.get(slug=slug)
    
    context = {'otour':otour, }
    return render(request, 'outbounds/outbounds-details.html', context)

def ocheckout(request, slug):
    
    
    otour = Otour.objects.get(slug=slug)
    
    current_user = request.user.customer
    tax = 0
    grand_total = 0
    total = 0
    
    if request.method == 'POST':
        form = ObookingForm(request.POST)
        if form.is_valid():

            data = Obooking()
            data.user =  current_user
            data.first_name = form.cleaned_data["first_name"]
            data.last_name = form.cleaned_data["last_name"]
            data.phone = form.cleaned_data["phone"]
            data.email = form.cleaned_data["email"]
            
            data.country = form.cleaned_data["country"]
            data.booking_note = form.cleaned_data["booking_note"]
            data.paymentMode = form.cleaned_data["paymentMode"]
            data.booking_total = grand_total
            data.tax  = tax
            data.otour= otour
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
            
            booking = Obooking.objects.get(user=current_user, is_booked=False, booking_number = booking_number)
            
            # after Booking done send email to Customer
            html_template = 'outbounds/booking_email.html'
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
            
            
            
            
            
            context = {
                'booking' : booking,
                
                'total': total,
                'tax' : tax,
                'grand_total' : grand_total,
                
                

            }
            return render(request, 'bookings/confirmation.html', context)

        else:
            return HttpResponse('Booking not saved')
                           
    
    
    context = {'otour':otour}
    return render (request, 'outbounds/ocheckout.html', context)

    
   
        



def createObooking(request):
        pass
    
# Otour Booking     
def Oconfirmation(request):
    
    context = {}
    return redirect(request, 'outbounds/confirmation.html', context)


    
    

def Oinvoice(request):
    pass