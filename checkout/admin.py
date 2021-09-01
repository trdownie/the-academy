from django.contrib import admin
from .models import Order

class OrderLineAdminInLine(admin.TabularInline):
    model = Order.order_items.through

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineAdminInLine,)

    exclude = ('order_items',)

    readonly_fields = ('order_number', 'date', 'order_total',)

    fields = ('order_number', 'date', 'full_name', 'email', 'order_total',)

    list_display = ('order_number', 'date', 'full_name', 'email', 'order_total',)

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)