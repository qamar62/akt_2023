from django.shortcuts import render, redirect
from .forms import ContactusForm
from frontend.models import Faq, FaqServices, HappyCutomer, Newsletter
from tour.models import Tour , Promotion
from accounts.models import  Contact
from django.contrib import messages
from django.core.mail import send_mail
from outbounds.models import Otour

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.db.models import Q
from tour.models import ReviewRating
from tour.forms import ReviewForm
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import time
# Create your views here.


def front(request):

    tours = Tour.objects.all()
    discount = Promotion.objects.all
    total_tours = tours.count()
    happy_customer = HappyCutomer.objects.all()


    context = {'tours': tours , 'discount': discount, 'total_tours':total_tours, 'happy_customer':happy_customer}
    return render(request, "frontend/home.html", context)



def gallery(request):
    
    context = {}
    return render(request, 'frontend/gallery.html' , context)
    
    
    
def contactUs(request):

    if request.method=="POST":
      form=ContactusForm(request.POST)
      if form.is_valid():
            messages.success(request, 'Message sent successfully!')
            form.save()
            time.sleep(3)
      else:
          messages.info(request, 'Something Wrong! Please try again')
            
            
    form=ContactusForm()

    context = {'form': form}
    return render(request, "frontend/contact.html", context)




def aboutUs(request):

    
    context = {}
    return render(request, "frontend/about.html", context)





def faq(request):
    faq_services = FaqServices.objects.all()
    faqs = Faq.objects.all()
    context = {'faqs':faqs, 'faq_services':faq_services}
    return render(request, "frontend/faqs.html", context)

def privacyPage(request):
    
    context = {}
    return render(request, "frontend/privacy-policy.html", context)
    





def successPage(request):


    context = {}
    return render(request, 'frontend/success_page.html', context)


def handle404(request, exception ):
    
    return render(request,'frontend/404.html', status=404)

def newsletter(request):
    if request.method == "POST":
        email = request.POST['email_newsletter_2']
        
        if Newsletter.objects.filter(email=email).exists() :
            messages.info(request, "Email already registered")
        else :
            newsletter = Newsletter(email=email)
            newsletter.save()
            messages.success(request, "Thank you, Your Email has been successfully saved")
        
        # send email to cutomer 
        html_template = 'frontend/newsletter.html'
        subject = 'Thank you for subscribing!'
        html_message = render_to_string(html_template, {
            'user': request.user,
            
        })
        recipient_list = [email]
        email_from = settings.EMAIL_HOST_USER
        message = EmailMessage(subject, html_message, email_from, recipient_list)
        message.content_subtype = "html"
        message.send()
        return redirect('home')

def cate_link(request):
    links =  Tour.objects.all()
    return dict(links = links)

def error_404(request, exception):


    context = {}
    return render(request, 'frontend/404.html', context)





def search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        tours= Tour.objects.order_by('-date_created').filter(Q(description__icontains=q) | Q(name__icontains=q))
        otours= Otour.objects.order_by('-date_created').filter(Q(description__icontains=q) | Q(name__icontains=q))
        
        
    else:
        tours=Tour.objects.all()
        otours=Otour.objects.all()
    context = {'tours':tours, 'otours':otours}
    return render(request, 'frontend/search.html', context)