from multiprocessing import context
from django.shortcuts import render
from visa.forms import VisaForm

from visa.models import Visa

# Create your views here.


def visaDashboard(request):
    
    user = request.user
    visas = Visa.objects.all()

    context = {'visas':visas}
    return render( request, "visa/visaDashboard.html", context)

def addVisa(request):
    form = VisaForm()

    context = {'form':form}
    return render(request, "visa/add_visa.html", context)