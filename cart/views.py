from email import message
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ObjectDoesNotExist

from outbounds.models import Otour



from .models import Cart, CartItem
from tour.models import Extra, Tour
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart




@login_required(login_url="login")
def add_cart(request, tour_id):
    current_user = request.user
    tour =  Tour.objects.get(id=tour_id)
   
    
    if current_user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except:
            cart =  Cart.objects.create(
                cart_id = _cart_id(request),
            )
        cart.save()

    try:
        cart_item =  CartItem.objects.get( tour=tour,  cart=cart)
        cart_item.adult_quantity += 1 
         
        cart_item.save()

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            tour = tour,
           
            adult_quantity = 1,
            child_quantity = 0,
            cart = cart,
        )
    cart_item.save()

    return redirect('cart')

def add_cart_child(request, tour_id):
    tour =  Tour.objects.get(id=tour_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
   
    cart_item =  CartItem.objects.get(tour=tour, cart = cart)
    cart_item.child_quantity += 1 
        
    cart_item.save()

    
    return redirect('cart')






def remove_cart(request, tour_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    tour = get_object_or_404(Tour, id=tour_id)
    
    
    cart_item = CartItem.objects.get(tour=tour, cart=cart)
    if cart_item.adult_quantity > 1 :
        cart_item.adult_quantity-= 1
        
        cart_item.save()
    
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_child(request, tour_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    tour = get_object_or_404(Tour, id=tour_id)
    cart_item = CartItem.objects.get(tour=tour, cart=cart)
    if cart_item.child_quantity > 1 :
        cart_item.child_quantity-= 1
        
        cart_item.save()
    
    else:
        cart_item.child_quantity = 0
        cart_item.save()
    return redirect('cart')

def remove_cart_item(request, tour_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    tour = get_object_or_404(Tour, id=tour_id)
    cart_item = CartItem.objects.get(tour=tour, cart=cart)
    cart_item.delete()
    return redirect('cart')


@login_required(login_url="login")
def cart(request, total=0, cart_items=None):
    
    try:
        tax = 0
        grand_total = 0
        user = request.user
        
        cart_items =  CartItem.objects.filter(user=user, is_active=True)
            
         
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        
           
            
            
        tax = (5 * total)/100
        grand_total =  total + tax

    except ObjectDoesNotExist:
        pass

    
    
    
    context = {
        'total' : total,
        
        
        'cart_items': cart_items,
        'tax' : tax,
        'grand_total' : grand_total,
        
    }
    return render(request, 'cart/cart.html', context)


@login_required(login_url="login")
def checkout(request, total=0, cart_items=None):



    try:
        tax = 0
        grand_total = 0
        
        cart_items =  CartItem.objects.filter(user=request.user, is_active=True)
            
         
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        
        
            
        tax = (5 * total)/100
        grand_total =  total + tax  

    except ObjectDoesNotExist:
        pass
    
    
    


    
    
    context = {
        'total' : total,
       
        'cart_items': cart_items,
        'tax' : tax,
        'grand_total' : grand_total,
        
        
    }
    return render (request,  'cart/checkout.html', context)

def success(request):
    context = {}
    return render (request, 'cart/confirmation.html', context)