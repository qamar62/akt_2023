from django import forms

from accounts.models import Contact

from captcha.fields import ReCaptchaField

class ContactusForm(forms.ModelForm):
    
    
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['name'].widget.attrs.update({ 
            'class': 'form-control bg_input', 
            'required':'required', 
            'name':'fullname', 
            'type':'text', 
            'placeholder':'User Name',
            
            }) 
            
        self.fields['email'].widget.attrs.update({ 
            'class': 'form-control bg_input', 
            'required':'required', 
            'name':'fullname', 
            'type':'email', 
            'placeholder':'Email', 
            }) 
        self.fields['phone'].widget.attrs.update({ 
            'class': 'form-control bg_input', 
            'required':'required', 
            'name':'phone', 
            'type':'text', 
            'placeholder':'Phone ', 
            }) 
        self.fields['message'].widget.attrs.update({ 
            'class': 'form-control  bg_input', 
            'required':'required', 
            'name':'message', 
            'type':'text', 
            'placeholder':'Message ', 
            }) 
        self.fields['captcha'].widget.attrs.update({ 
            'class': 'form-control  bg_input', 
            
             
            
            }) 
                   
            
    
    
    
    captcha=ReCaptchaField()
    class Meta:
        model = Contact
        fields = ['name', 'phone', 'email', 'message','captcha']