from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Customer, Category, Product, Order, OrderItem
from django.contrib.auth.admin import UserAdmin

@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("phone", "address")}),
    )


admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Product)
admin.site.register(Order)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("unit_price",)
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "created_at", "total_price")
    inlines = [OrderItemInline]




