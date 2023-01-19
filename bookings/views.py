import datetime

from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from bookings.forms import BookingForm
from bookings.models import BookTour, Booking, Payment, Obooking

from cart.models import Cart, CartItem
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from cart.views import _cart_id

# Create your views here.

def payments(request):
    body =  json.loads(request.body)
    booking = Booking.objects.get(user=request.user, is_booked=False, booking_number=body['bookingID'])

    # store transction detail inside payment model
    payment = Payment(
        user = request.user,
        payment_id  = body['transID'],
        payment_method =  body['payment_method'],
        amount_paid =  booking.booking_total,
        status = body['status'],

    )
    payment.save()

    booking.payment = payment
    booking.is_booked = True
    booking.save()
    
    # move the cart items to Booking tour 
    cart_items =  CartItem.objects.filter(user=request.user)

    for item in cart_items:
        booktour = BookTour()
        booktour.booking_id = booking.id
        booktour.payment = payment
        booktour.user_id = request.user.id
        booktour.tour_id = item.tour_id
        booktour.adult_quantity = item.adult_quantity
        booktour.child_quantity = item.child_quantity
        booktour.adult_price = item.tour.adult_price
        booktour.child_price = item.tour.child_price
        booktour.booked = True
        booktour.save()
    


    CartItem.objects.filter(user=request.user).delete()
    
    # email to customer 
    mail_subject = 'Thank you for your Booking!'
    message = render_to_string('bookings/booking_received_email.html', {
        'user': request.user,
        'booking': booking,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    data = {
        'booking_number': booking.booking_number,
        'transID' : payment.payment_id,
        
    }
    
    return JsonResponse(data)
    

def create_booking(request, total=0,adult_quantity=0, child_quantity=0):
    current_user = request.user.customer

    
    cart_items = CartItem.objects.filter(user=current_user)
    # cart_count = cart_items.count()
    # if cart_count <= 0:
    #     return redirect('home')
   
    
    try:
        tax = 0
        grand_total = 0
        cart_items =  CartItem.objects.filter(user=request.user.cusotmer, is_active=True)
                
            
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            total += (cart_item.tour.adult_price * cart_item.adult_quantity)
            adult_quantity += cart_item.adult_quantity
            total += (cart_item.tour.child_price * cart_item.child_quantity)
            child_quantity += cart_item.child_quantity
        
        tax = (5 * total)/100
        grand_total =  total + tax
        print(grand_total)
    except:
        pass
        
    

    
   
        

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():

            data = Booking()
            data.user =  current_user
            data.first_name = form.cleaned_data["first_name"]
            data.last_name = form.cleaned_data["last_name"]
            data.phone = form.cleaned_data["phone"]
            data.email = form.cleaned_data["email"]
            data.pickup_location = form.cleaned_data["pickup_location"]
            data.country = form.cleaned_data["country"]
            data.booking_note = form.cleaned_data["booking_note"]
            data.paymentMode = form.cleaned_data["paymentMode"]
            data.booking_total = grand_total
            data.tax  = tax
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
            context = {
                'booking' : booking,
                'cart_items': cart_items,
                'total': total,
                'tax' : tax,
                'grand_total' : grand_total,
                "adult_quantity": adult_quantity,
                "child_quantity" : child_quantity,
                

            }
            return render(request, 'bookings/payments.html', context)

    else:
        return redirect('checkout')
    

    
def booking_complete(request):
    booking_number = request.GET.get('booking_number')
    transID = request.GET.get('payment_id')
    try:
        booking =  Booking.objects.get(booking_number=booking_number, is_booked = True)
        booked_tours = BookTour.objects.filter(booking_id=booking.id)
        
        subtotal = 0
        for i in booked_tours:
            subtotal += i.adult_price * i.adult_quantity
            subtotal += i.child_price * i.child_quantity
        
        payment = Payment.objects.get(payment_id=transID)

        context = {
            'booking':booking,
            'booked_tours':booked_tours,
            'booking_number':booking.booking_number,
            'transID': payment.payment_id,
            'payment':payment,
            'subtotal':subtotal,
            

        }
        return render(request, 'bookings/confirmation.html', context)
    except (Payment.DoesNotExist , Booking.DoesNotExist):
        return redirect('home')


def viewBooking(request, id):
    bookings = Obooking.objects.get(id=id)
    
    
    context = {'bookings':bookings}
    return render(request, 'bookings/viewBooking.html', context)

def viewTourBooking(request, id):
    
    bookings = Booking.objects.get(id=id)
    
    
    context = {'bookings':bookings}
    return render(request, 'bookings/viewTourBooking.html', context)

def invoice(request):
    context = {}
    return render(request, 'bookings/invoice.html', context)
