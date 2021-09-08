from django.contrib import admin
from .models import Order

class OrderLineAdminInLine(admin.TabularInline):
    model = Order.order_items.through

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineAdminInLine,)

    exclude = ('order_items',)

    readonly_fields = ('order_number', 'date', 'order_total',
                       'original_bag', 'stripe_pid')

    fields = ('order_number', 'academic', 'order_total', 'date', 'full_name',
              'email', 'phone_number', 'street_address1',
              'street_address2', 'town_or_city', 'postcode',
              'county', 'country', 'original_bag', 'stripe_pid')

    list_display = ('order_number',  'order_total', 'date',
                    'full_name', 'email',)

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)