from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """
    OrderForm maps to the Order class and is used for
    capturing order details and customer info
    """

    class Meta:
        model = Order
        # Specify fields
        fields = ('full_name', 'email', 'phone_number', 
                  'street_address1', 'street_address2', 'town_or_city',
                  'postcode', 'county', 'country',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define placeholders
        placeholders = {
                'full_name': 'Full Name',
                'email': 'Email Address',
                'phone_number': 'Phone Number',
                'street_address1': 'Street Address 1',
                'street_address2': 'Street Address 2',
                'town_or_city': 'Town or City',
                'postcode': 'Post Code',
                'county': 'County',
        }

        # Set autofocus on first input & labels
        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            label = labels[field]
            self.fields[field].label = label
