
from django import forms

class FormClass(forms.Form):
    image = forms.FileField()
    text = forms.CharField(max_length=100,label="First name")
    text2 = forms.CharField(max_length=100,label="Last name")
    email = forms.EmailField(label='Email')