from django import forms
from .models import Article, Subject


class ArticleForm(forms.ModelForm):
    """
    ArticleFrom maps to the Article class and is used
    for creating and updating article intances
    """

    class Meta:
        model = Article
        exclude = ('stakers',)  # calculated backend on order

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        subjects = Subject.objects.all()
        friendly_names = [
            (s.id, s.get_friendly_name().capitalize()) for s in subjects]

        # Render friendly names on the form
        self.fields['subjects'].choices = friendly_names

        # Define placeholders
        placeholders = {
                'image': 'Image',
                'title': 'Title*',
                'subjects': 'Subjects*',
                'authors': 'Authors* (author consent required',
                'article': 'Article or Proposal*',
                'date': "Date Published* (today for proposals)",
                'summary': 'Summary*',
                'price': 'Price or Stake*',
                'rating': 'Rating (if known)',
        }

        # Set title for proposal as check box
        self.fields['proposal'].label = 'PROPOSAL ONLY'

        # Set placeholders & remove titles for all others
        for field in self.fields:
            if field != 'proposal':
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].label = False
