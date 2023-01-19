from . models import B2bAgent
from django.forms import ModelForm


class B2bRegistrationForm(ModelForm):
    
   
    
    # def __init__(self, *args, **kwargs): 
    #     super().__init__(*args, **kwargs) 
    #     self.fields['username'].widget.attrs.update({ 
    #         'class': 'form-control', 
    #         'required':'required', 
    #         'name':'username', 
    #         'id':'username', 
    #         'type':'text', 
    #         'placeholder':'User Name', 
            
    #         }) 
        
    
    
    
    
    
    class Meta:
        model = B2bAgent
        fields = '__all__'