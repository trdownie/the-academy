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

        # Define placeholders & labels
        placeholders = {
            'title': 'Title*',
            'authors': 'Authors* (author consent required',
            'subjects': 'Subjects*',
            'date': "Date Published* (today for proposals)",
            'summary': 'Summary*',
            'price': 'Price or Stake*',
            'rating': 'Rating (if known)',
        }
        labels = {
            'proposal': 'PROPOSAL ONLY',
            'article': 'UPLOAD ARTICLE/PROPOSAL',
            'image': 'UPLOAD COVER IMAGE (RECOMMENDED)',
        }

        # Set placeholders or labels depending on field
        for field in self.fields:
            if field in placeholders:
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].label = False
            elif field in labels:
                label = labels[field]
                self.fields[field].label = label

