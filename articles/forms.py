from django import forms
from .widgets import CustomClearableFileInput
from .models import Article, Subject


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = '__all__'

    image = forms.ImageField(label='Image', required=False,
                             widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        subjects = Subject.objects.all()
        friendly_names = [(s.id, s.get_friendly_name()) for s in subjects]

        self.fields['subjects'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'tbc'

        self.fields['proposal'].label = 'PROPOSAL ONLY'
        self.fields['title'].label = 'Title*'
        self.fields['subjects'].label = 'Subjects*'
        self.fields['authors'].label = 'Authors* (Note: adding authors without their consent can lead to article rejection)'
        self.fields['article'].label = 'Article or Proposal*'
        self.fields['date'].label = "Date Published* (Note: use today's date for for proposals)"
        self.fields['summary'].label = "Summary*"
        self.fields['price'].label = "Price or Stake*"