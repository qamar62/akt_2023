from django.shortcuts import render, redirect



from . models import Transfer
import datetime
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.


def transfer(request):
    
    transfers = Transfer.objects.all()
    
    paginator = Paginator(Transfer.objects.all(), 3)
    page =  request.GET.get('page')
    paged_tours =  paginator.get_page(page)
    
    
    context = {'transfers':transfers}
    return render(request, 'transfer/transfers.html', context)



def transferDetail(request, slug):
     
    
    transfers = Transfer.objects.get(slug=slug)
    
    context = {'transfers': transfers,}
    return render(request, 'transfer/transfer_detail.html', context)

def tcheckout(request):
    
    context = {}
    return render(request, 'transfer/tcheckout.html', context)

def tConfirmation(request):
    
    context = {}
    return render(request, 'transfer/tconfirmation.html', context)