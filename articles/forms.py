from django import forms
from .models import Article, Subject


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        exclude = ('stakers',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        subjects = Subject.objects.all()
        friendly_names = [
            (s.id, s.get_friendly_name().capitalize()) for s in subjects]

        # Render friendly names on the form
        self.fields['subjects'].choices = friendly_names

        # Replace labels with tailored labels
        self.fields['proposal'].label = 'PROPOSAL ONLY'
        self.fields['title'].label = 'Title*'
        self.fields['subjects'].label = 'Subjects*'
        self.fields['authors'].label = 'Authors* (Note: adding authors without \
                                their consent can lead to article rejection)'
        self.fields['article'].label = 'Article or Proposal*'
        self.fields['date'].label = "Date Published* (Note: use today's date \
                                for for proposals)"
        self.fields['summary'].label = "Summary*"
        self.fields['price'].label = "Price or Stake*"
