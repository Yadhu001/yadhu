from django import forms
from.models import *
class updateform(forms.ModelForm):
    class Meta:
        model=product
        fields='__all__'