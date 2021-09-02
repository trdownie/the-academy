import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from articles.models import Article


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, blank=True)
    county = models.CharField(max_length=80, blank=True)
    order_items = models.ManyToManyField(Article)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)


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
        self.order_total = sum(Article.price for article in self.order_items.through.all())
    
    
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
        Ser order number if not yet set
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number