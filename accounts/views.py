from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.contrib import messages
from accounts.signals import customer_profile

from cart.apps import CartConfig
from cart.models import Cart, CartItem
from cart.views import _cart_id
from outbounds.models import Otour

from .models import *
from tour.models import  Tour
from bookings.models import  Booking
from .forms import CreateUserForm, CustomerForm
from .decorators import unauthenticated_user, allowed_users, admin_only





@unauthenticated_user
def registerPage(request):
   
    form = CreateUserForm(request.POST)
    
    
    if form.is_valid():
        
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        email = form.cleaned_data.get("email")
       
        form.save()
        messages.success(request, "Accounts was created successfully , to varify your account kindly reconfirm your email")
        
        new_user = authenticate(username=username, password=password)
        if new_user is not None:
        
            login(request, new_user)
            redirect('login')
    form = CreateUserForm()
  
    
    context = {'form':form}
    return render(request, 'accounts/register.html', context)



def account_vertify(request, token):
    pf =  Customer.objects.filter(email_token=token).first()
    pf.is_varified = True
    pf.save()
    messages.success(request, "Congratulaition! Your accounts has been verified")
    
    return redirect('register')



@unauthenticated_user
def loginPage(request):
    
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)
        prof = Customer.objects.get(user=user)
        if prof.is_varified:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, "Account not Verified, kinldy check your email")
            return redirect('login')
        # if user is not None:
        #     try : 
        #         cart =  Cart.objects.get(cart_id = _cart_id(request))
        #         is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
        #         if is_cart_item_exists :
        #             cart_item = CartItem.objects.filter(cart=cart)

        #             for item in cart_item:
        #                 item.user = user
        #                 item.save()
        #     except:
        #         pass
        #     login(request, user)
        #     return redirect('home')
        # else:
        #     messages.info(request, "Username Or Password is incorrect")   
            
            
        
        
    

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')




# @login_required(login_url='login')
# @admin_only
# def home(request):
#     bookings = Booking.objects.all()
#     customers = Customer.objects.all()

#     total_customers = customers.count()

#     total_bookings = bookings.count()
#     pending = bookings.filter(status = 'Payment Pending').count()
#     booked = bookings.filter(status = 'Booked').count()
#     reconfirmed = bookings.filter(status = 'Reconfirmed').count()

#     context = {'bookings':bookings, 'customers':customers, 
#                 'total_customers':total_customers,
#                 'total_bookings': total_bookings, 
#                 'pending':pending,
#                 'booked':booked,
#                 'reconfirmed':reconfirmed,
#     }
#     return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])
def userPage(request):
    wishlist = Otour.objects.filter(user_wishlist=request.user)
    bookings = request.user.customer.booking_set.all()


    total_bookings = bookings.count()
    pending = bookings.filter(status = 'Payment Pending').count()
    booked = bookings.filter(status = 'Booked').count()
    reconfirmed = bookings.filter(status = 'Reconfirmed').count()
    
    
   
    
    customer = request.user.customer
    form = CustomerForm(instance = customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'bookings':bookings,
                'total_bookings': total_bookings, 
                'pending':pending,
                'booked':booked,
                'reconfirmed':reconfirmed,
                'form':form,
                'customer':customer,
                'wishlist':wishlist
    
    }
    
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    wishlist = Otour.objects.filter(user_wishlist=request.user)
    bookings = request.user.customer.booking_set.all()


    total_bookings = bookings.count()
    pending = bookings.filter(status = 'Payment Pending').count()
    booked = bookings.filter(status = 'Booked').count()
    reconfirmed = bookings.filter(status = 'Reconfirmed').count()
    
    
    customer = request.user.customer
    form = CustomerForm(instance = customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form, 
               'bookings':bookings,
                'total_bookings': total_bookings, 
                'pending':pending,
                'booked':booked,
                'reconfirmed':reconfirmed,
                'form':form,
                'customer':customer,
                'wishlist':wishlist
               
               }
    return render(request, 'accounts/my-profile.html', context)



@login_required(login_url='login')
@admin_only
def customer(request, pk):
    customer = Customer.objects.get(id = pk)
    bookings = customer.booking_set.all()
    booking_count = bookings.count()

    
    
    context = {'customer':customer, 'bookings':bookings, 'booking_count':booking_count,
                
                }
    return render(request, 'accounts/customers.html', context)


@login_required(login_url='login')
def status(request):
    return render(request, 'accounts/status.html')

@login_required(login_url='login')
@admin_only
def tours(request):
    tours = Tour.objects.all()
    return render(request, 'accounts/tours.html', {'tours': tours})

# def search_tours(request):
#         if request.method == 'GET':
#             form = SearchTourForm(request.GET)
#             if form.is_valid():
#                 Country = form.cleaned_data['Country']
#                 Type = form.cleaned_data['Type']
#                 Destination = form.cleaned_data['Destination']
#                 StartDate = form.cleaned_data['StartDate']

#                 tours = Tour.objects.filter(Q(Country__icontains = Country)|
#                                     Q(Type__exact = int(Type))|
#                                     Q(Destination__exact = int(Destination))|
#                                     Q(StartDate__gte = int(StartDate)))

#                 return render(request, 'tours/search_tours.html', {
#                     'tours': tours,
#                     'media_url': settings.MEDIA_URL,
#                     'form':form,
#                 })

#         else:
#             form = SearchTourForm()

#         tours = Tour.objects.filter(Available = True)


#         return render(request, 'tours/search_tours.html', {
#             'tours': tours,
#             # 'media_url': settings.MEDIA_URL,
#             'form':form,
#         })