from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# Extend default user for Customers
class Customer(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


# Category with hierarchy (self-referencing)
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    def __str__(self):
        return self.name


# Product
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.name


# Order
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"
