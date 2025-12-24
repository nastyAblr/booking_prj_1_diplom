
from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['booking', 'nights', 'cost']
    readonly_fields = ['nights', 'cost']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'created', 'is_active', 'total_cost']
    readonly_fields = ['created', 'updated']

    inlines = [OrderItemInline]

    def total_cost_display(self, obj):
        return obj.total_cost

    total_cost_display.short_description = 'Сумма заказа'

