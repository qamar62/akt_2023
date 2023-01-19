from django.shortcuts import render, redirect
from bookings.forms import TransferForm

from bookings.models import TransferBooking
from . models import Transfer
import datetime
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.


def transfer(request):
    
    transfers = Transfer.objects.all()
    
    
    context = {'transfers':transfers}
    return render(request, 'transfer/all_transfer_list.html', context)



def transferDetail(request):
    
    
    transfers = Transfer.objects.all()
    paginator = Paginator(Transfer.objects.all(), 3)
    page =  request.GET.get('page')
    paged_tours =  paginator.get_page(page)
    transfer_count =  transfers.count()
    
    current_user = request.user
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():

            data = TransferBooking()
            data.user =  current_user
            data.fullname = form.cleaned_data["fullName"]
            data.fullname = form.cleaned_data["service_date"]
            data.fullname = form.cleaned_data["service_time"]
            data.phone = form.cleaned_data["phone"]
            data.email = form.cleaned_data["email"]
            data.pickup_location = form.cleaned_data["pickup_location"]
            data.paymentMode = form.cleaned_data["paymentMode"]
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
            messages.success(request, "Your Tranfer  has been successfully Booked")
            return redirect('t-confirmation')
        else:
            messages.info(request, "Transfer Not saved")
            return redirect('transfer')
            
            
            
            
            
            
            
            
    
    context = {'transfers': paged_tours, 't_count':transfer_count}
    return render(request, 'transfer/transfer_detail.html', context)

def tcheckout(request):
    
    context = {}
    return render(request, 'transfer/tcheckout.html', context)

def tConfirmation(request):
    
    context = {}
    return render(request, 'transfer/tconfirmation.html', context)