from django.urls import path
from django.conf.urls import handler404
from . import views


urlpatterns = [
    path("", views.front, name="home"),
    path("activity/<str:slug>/", views.tourDetail, name="tour-detail"),
    path("tours/list/", views.toursList, name="all-tours-list"),
    path("tours/grid/", views.toursGrid, name="all-tours-grid"),
    path("contact/", views.contactUs, name="contact"),
    path("faq/", views.faq, name="faq"),
    path("about/", views.aboutUs, name="about"),
    path("gallery/", views.gallery, name="gallery"),
    path('submit_review/<int:tour_id>/' ,views.submit_review, name='submit_review'),
    
    path('newsletter/' ,views.newsletter, name='newsletter'),
    path('search-result/' ,views.search, name='search-page'),
    
    
    
]
handler404 = views.handle404