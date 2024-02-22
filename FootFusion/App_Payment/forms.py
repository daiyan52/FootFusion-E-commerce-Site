from django import forms
from .models import billingAddress

class billingAddressForm(forms.ModelForm):
    class Meta:
        model = billingAddress

        fields = ['city', 'zipcode', 'country', 'phone', 'address']
        