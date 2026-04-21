from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

User = get_user_model()


# =====================================================
# 🛍 PRODUCT LIST (PUBLIC GET)
# =====================================================
@api_view(["GET"])
@permission_classes([AllowAny])
def product_list(request):
    products = Product.objects.all().order_by("-created_at")
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


# =====================================================
# 🛍 CREATE PRODUCT (AUTH REQUIRED)
# =====================================================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_product(request):
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(vendor=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =====================================================
# 🛍 PRODUCT DETAIL
# =====================================================
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([AllowAny])
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    if request.method == "PUT":
        if product.vendor != request.user:
            return Response({"error": "Not allowed"}, status=403)

        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    if request.method == "DELETE":
        if product.vendor != request.user:
            return Response({"error": "Not allowed"}, status=403)

        product.delete()
        return Response({"message": "Deleted"})


# =====================================================
# 📂 CATEGORIES
# =====================================================
@api_view(["GET"])
@permission_classes([AllowAny])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)