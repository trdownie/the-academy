from django.db import models


class Academic(models.Model):
    name = models.CharField(max_length=70)
    username = models.CharField(max_length=15)
    about = models.TextField()
    level = models.DecimalField(max_digits=4, decimal_places=1, blank=True)
    image = models.ImageField(blank=True)
    following = models.ManyToManyField('self', symmetrical=False, blank=True)
    subscribers = models.DecimalField(max_digits=9, decimal_places=0, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
