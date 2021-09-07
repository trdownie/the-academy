from django import forms
from .models import Academic


class AcademicProfileForm(forms.ModelForm):
    class Meta:
        model = Academic
        exclude = ('user', 'level', 'following', 'subscribers',)
        
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
                'username': 'Username',
                'image': 'Image',
                'name': 'Full Name',
                'default_email': 'Email Address',
                'default_phone_number': 'Phone Number',
                'default_street_address1': 'Street Address 1',
                'default_street_address2': 'Street Address 2',
                'default_town_or_city': 'Town or City',
                'default_postcode': 'Post Code',
                'default_county': 'County',
                'about': 'About',
        }

        # Not working
        self.fields['about'].widget = forms.Textarea(
            attrs={'rows': 6, 'cols': 25})

        self.fields['name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
