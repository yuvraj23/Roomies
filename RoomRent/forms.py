from django import forms
from RoomRent.models import *
from django.contrib.auth.models import User




class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User

        fields=['username','first_name','last_name','email','password']




"""
from RoomRent.models import Text
class TextForm(forms.ModelForm):
    class Meta:
        model=Text
        fields=('body',)
        widgets = {
          'body': forms.Textarea(attrs={'rows':8, 'cols':50},),
        }
"""
