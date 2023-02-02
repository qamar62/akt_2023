from django.urls import path
from django.conf.urls import handler404
from . import views


urlpatterns = [
    path("", views.front, name="home"),
    
    path("contact/", views.contactUs, name="contact"),
    path("faq/", views.faq, name="faq"),
    path("about/", views.aboutUs, name="about"),
    path("privacy/", views.privacyPage, name="privacy"),
    path("gallery/", views.gallery, name="gallery"),
    
    
    path('newsletter/' ,views.newsletter, name='newsletter'),
    path('search-result/' ,views.search, name='search-page'),
    
    
    
]
handler404 = views.handle404