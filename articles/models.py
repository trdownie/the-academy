from django.db import models
from django.utils.translation import gettext_lazy as _

from academics.models import Academic


class Subject(models.Model):

    subject_name = models.CharField(max_length=200, null=False, blank=False)
    friendly_name = models.CharField(max_length=200, blank=True)

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

    class Meta:
        ordering = ['subject_name']

    def __str__(self):
        return self.subject_name

    def get_friendly_name(self):
        return self.friendly_name


class Article(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Academic)  # ['Einstein', 'Tesla', etc.]
    subjects = models.ManyToManyField(Subject)  # ['history', 'maths', etc.]
    article = models.FileField(upload_to='uploads/')
    date = models.DateField()
    summary = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
    image = models.ImageField(blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
