from django import forms

from accounts.models import Contact



class ContactusForm(forms.ModelForm):
    
    
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['name'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'required', 
            'name':'fullname', 
            'type':'text', 
            'placeholder':'User Name', 
            }) 
            
        self.fields['email'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'required', 
            'name':'fullname', 
            'type':'email', 
            'placeholder':'Email', 
            }) 
        self.fields['phone'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'required', 
            'name':'phone', 
            'type':'text', 
            'placeholder':'Phone ', 
            }) 
        self.fields['message'].widget.attrs.update({ 
            'class': 'form-control mb-3', 
            'required':'required', 
            'name':'message', 
            'type':'text', 
            'placeholder':'Message ', 
            }) 
                   
            
    
    
    
    
    class Meta:
        model = Contact
        fields = ['name', 'phone', 'email', 'message', ]