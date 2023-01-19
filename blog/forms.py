from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'title_tag', 'author', 'body')

        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
            'title_tag' : forms.TextInput(attrs={'class': 'form-control'}),
            'author' : forms.Select(attrs={'class': 'form-control'}),
            'body' : forms.Textarea(attrs={'class': 'form-control'}),
        }


class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'title_tag', 'body')

        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
            'title_tag' : forms.TextInput(attrs={'class': 'form-control'}),
            
            'body' : forms.Textarea(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['name'].widget.attrs.update({ 
            'class': 'form-control style_2"', 
            'required':'required', 
            'name':'name', 
             
            'type':'text', 
            'placeholder':'Enter name', 
            
            }) 
        self.fields['body'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'required', 
            'name':'message', 
             
            'type':'text', 
            'placeholder':'Message', 
            }) 
        
    
    
    
    
    
    class Meta:
        model = Comment
        fields = ["name", "body", ]
            
            