from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Avg, F
from .models import Category, Product, Order
from .serializers import (CategorySerializer, ProductSerializer, OrderCreateSerializer, OrderDetailSerializer,)



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def average_price(self, request, pk=None):
        """
        Returns average product price for this category including all descendant categories.
        """
        category = self.get_object()
        # Get subtree categories (including self) using mptt
        subtree = category.get_descendants(include_self=True)
        # products across subtree
        average = Product.objects.filter(category__in=subtree).aggregate(avg_price=Avg("price"))["avg_price"]
        if average is None:
            return Response({"category": category.name, "average_price": None})
        return Response({"category": category.name, "average_price": float(round(average, 2))})


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class OrderViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        out = OrderDetailSerializer(order).data
        return Response(out, status=status.HTTP_201_CREATED)

    def list(self, request):
        # list orders for the authenticated user
        qs = Order.objects.filter(customer=request.user).prefetch_related("items__product")
        serializer = OrderDetailSerializer(qs, many=True)
        return Response(serializer.data)


class ProtectedHello(api_view):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({"message": f"Hello, {user.username}. You are authenticated."})