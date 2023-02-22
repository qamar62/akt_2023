
from django import forms
from .models import Inquiry
from captcha.fields import ReCaptchaField




class InquiryForm(forms.ModelForm):
    captcha=ReCaptchaField()
    class Meta:
        model = Inquiry
        fields = ['fullname', 'mobile', 'email', 'message','captcha']

