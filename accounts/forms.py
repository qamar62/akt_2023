from email.policy import default
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from django import forms
from .models import *


class CustomerForm(ModelForm):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['name'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'required', 
            'type':'text', 
            }) 
             
        self.fields['phone'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'required', 
            'type':'text', 
            }) 
             
             
        self.fields['email'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'required', 
            'type':'email', 
            }) 
       
        
            
            
             
            
             
             
            
       
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'email_token', 'is_varified']







class CreateUserForm(UserCreationForm):
    
   
    
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['username'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'required', 
            'name':'username', 
            'id':'username', 
            'type':'text', 
            'placeholder':'User name*', 
            
            }) 
        self.fields['email'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'required', 
            'name':'email', 
            'id':'email', 
            'type':'email', 
            'placeholder':'Email Address', 
            }) 
        self.fields['password1'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'required', 
            'name':'password1', 
            'id':'password1', 
            'type':'password', 
            'placeholder':'Password', 
            }) 
        self.fields['password2'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'required', 
            'name':'password2', 
            'id':'password2', 
            'type':'password', 
            'placeholder':'Retype Password', 
            }) 
    
    
    
    
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]