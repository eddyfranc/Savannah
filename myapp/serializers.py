from rest_framework import serializers
from .models import Category, Product, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "parent", "children")
        read_only_fields = ("children",)

    def get_children(self, obj):
        # provide direct children for convenience (not full tree)
        return CategorySerializer(obj.get_children(), many=True).data


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ("id", "name", "price", "category", "description", "created_at")
        read_only_fields = ("created_at",)


class OrderItemCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    class Meta:
        model = OrderItem
        fields = ("product", "quantity")


class OrderCreateSerializer(serializers.Serializer):
    items = OrderItemCreateSerializer(many=True)

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must contain at least one item.")
        return value

    def create(self, validated_data):
        request = self.context.get("request")
        customer = request.user
        items_data = validated_data["items"]

        from django.db import transaction
        order = None
        with transaction.atomic():
            order = Order.objects.create(customer=customer, total_price=0)
            total = 0
            for item in items_data:
                product = item["product"]
                quantity = item.get("quantity", 1)
                unit_price = product.price
                oi = OrderItem.objects.create(
                    order=order, product=product, quantity=quantity, unit_price=unit_price
                )
                line_total = unit_price * quantity
                total += line_total
            order.total_price = total
            order.save()
        return order


class OrderDetailItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ("product", "quantity", "unit_price", "line_total")

    def get_line_total(self, obj):
        return obj.unit_price * obj.quantity


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderDetailItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "customer", "created_at", "total_price", "items")
