import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from articles.models import Article
from academics.models import Academic


class Order(models.Model):
    academic = models.ForeignKey(Academic, on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 related_name='orders')
    order_number = models.CharField(max_length=32, null=False, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, blank=True)
    county = models.CharField(max_length=80, blank=True)
    order_items = models.ManyToManyField(Article)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')


    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()


    def update_total(self):
        """
        update order total when saving Order
        """
        # self.order_total = self.order_items.aggregate(Sum('price'))['price__sum']
        # if self.pk is None:
        #    self.order_total = 0
        # else:
        self.order_total = sum(article.price for article in self.order_items.all())

    
    """
    FROM STACK OVERFLOW
    def order_total(self):
        queryset = self.order_items.all().aggregate(
            order_total=models.Sum('price'))
        return queryset["total_price"]
    """

    """
    def calculate_total(self):
        return sum(Article.price for article in self.order_items)
    """
    
    """
    def update_total(self):
        Update order total each time a line item is added
        self.order_total = self.order_items.aggregate(Sum('price'))
        self.save()
    """

    def save(self, *args, **kwargs):
        """
        Set order number if not yet set
        """
        if self.id:
            self.update_total()
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number
