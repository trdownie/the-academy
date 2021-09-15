import time

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField


class Academic(models.Model):
    # Profile Info
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='academic', null=True)
    name = models.CharField(max_length=70)
    username = models.CharField(max_length=15)  # to delete?

    # Contact Info
    default_email = models.EmailField(max_length=254, blank=True)
    default_phone_number = models.CharField(max_length=20, blank=True)

    # Billing Info
    default_street_address1 = models.CharField(max_length=80, blank=True)
    default_street_address2 = models.CharField(max_length=80, blank=True)
    default_town_or_city = models.CharField(max_length=40, blank=True)
    default_county = models.CharField(max_length=80, blank=True)
    default_postcode = models.CharField(max_length=20, blank=True)
    default_country = CountryField(blank_label='Country', blank=True)

    # Academic Info
    about = models.TextField()
    level = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    image = models.ImageField(blank=True)
    following = models.ManyToManyField('self', symmetrical=False, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_or_update_academic_profile(sender, instance, created, **kwargs):
    """
    Create or update  profile
    """
    if created:
        Academic.objects.create(user=instance, username=instance.username)
    # For existing users, just save profile
    instance.academic.save()
