from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Subject(models.Model):

    class ScienceArea(models.TextChoices):
        HUMAN = 'HU', _('Human')
        SOCIAL = 'SO', _('Social')
        NATURAL = 'NA', _('Natural')
        FORMAL = 'FO', _('Formal')
        APPLIED = 'AP', _('Applied')

    science = models.CharField(
        max_length=2,
        choices=ScienceArea.choices,
        blank=False,
    )

    subject = models.CharField(max_length=200, null=False, blank=False)
    friendly_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.subject

    def get_friendly_name(self):
        return self.friendly_name


class Article(models.Model):
    title = models.CharField(max_length=200)
    subjects = models.ManyToManyField(Subject)
    article = models.FileField(upload_to='uploads/')
    date = models.DateField()
    summary = models.TextField()
    rating = models.DecimalField(max_digits=5, decimal_places=1, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
    image_url = models.URLField(blank=True)
    image = models.ImageField(blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
