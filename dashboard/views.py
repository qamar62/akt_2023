from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import  allowed_users
from accounts.models import Customer
from bookings.models import Booking
from tour.models import Tour
from outbounds.models import  Otour

# Create your views here.

@login_required(login_url='login')

def dashboard(request):
    if request.user.is_staff:
        tours = Tour.objects.all()
        otours = Otour.objects.all()
        total_tours = tours.count()
        total_otours = otours.count()
    
        bookings = Booking.objects.all()
        customers = Customer.objects.all()

        total_customers = customers.count()

        total_bookings = bookings.count()
        pending = bookings.filter(status = 'Payment Pending').count()
        booked = bookings.filter(status = 'Booked').count()
        reconfirmed = bookings.filter(status = 'Reconfirmed').count()

        context = {'bookings':bookings, 'customers':customers, 
                    'total_customers':total_customers,
                    'total_bookings': total_bookings, 
                    'pending':pending,
                    'booked':booked,
                    'reconfirmed':reconfirmed,
                    'total_tours':total_tours,
                    'total_otours':total_otours,
                    
                    }
    
        return render(request , 'dashboard/index.html', context)
    else: 
        return redirect("user-page")


#Apps

def calendar(request):
    
    context={}
    return render(request , 'dashboard/apps-calendar.html', context)

def chat(request):
    
    context={}
    return render(request , 'dashboard/apps-chat.html', context)

def email(request):
    
    context={}
    return render(request , 'dashboard/apps-mailbox.html', context)

def task(request):
    
    context={}
    return render(request , 'dashboard/apps-tasks-list-view.html', context)

#project
def project(request):
    
    context={}
    return render(request , 'dashboard/apps-projects-list.html', context)

def createProject(request):
    
    context={}
    return render(request , 'dashboard/apps-projects-create.html', context)

# invoices
def invoiceList(request):
    
    context={}
    return render(request , 'dashboard/apps-invoices-list.html', context)

def invoiceDetail(request):
    
    context={}
    return render(request , 'dashboard/apps-invoices-details.html', context)

def invoiceCreate(request):
    
    context={}
    return render(request , 'dashboard/apps-invoices-create.html', context)

# support Ticket 
def supportTicketList(request):
    
    context={}
    return render(request , 'dashboard/apps-tickets-list.html', context)

def detailSupportTicket(request):
    
    context={}
    return render(request , 'dashboard/apps-tickets-details.html', context)