from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Customer, Category, Product, Order
from django.contrib.auth.admin import UserAdmin

@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("phone", "address")}),
    )

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
