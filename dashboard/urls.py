from django.urls import path
from . import views



urlpatterns = [
    path('', views.dashboard, name="dashboard"), 
    path('calendar', views.calendar, name="calendar"), 
    path('chat', views.chat, name="chat"), 
    path('mail', views.email, name="mailbox"), 
    path('task-list', views.task, name="task-list"), 
    path('project-list', views.project, name="project-list"), 
    path('project-create', views.createProject, name="project-create"), 
    #invoice
    path('invoices', views.invoiceList, name="invoices"), 
    path('detail-invoice', views.invoiceDetail, name="detail-invoice"), 
    path('create-invoice', views.invoiceCreate, name="create-invoice"), 
    
    # Support Ticket
    path('support-ticket', views.supportTicketList, name="support-ticket"), 
    path('detail-ticket', views.detailSupportTicket, name="detail-ticket"), 
    
      
]
