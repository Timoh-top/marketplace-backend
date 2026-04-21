from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Product, Category, Cart, CartItem, Review, Wishlist
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    ReviewSerializer,
    CartSerializer,
    WishlistSerializer,
    UserSerializer,
)

User = get_user_model()


# =====================================================
# 🔐 AUTH
# =====================================================
class MyTokenView(TokenObtainPairView):
    pass


# =====================================================
# 👤 REGISTER
# =====================================================
@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {
                "message": "User created successfully",
                "user": UserSerializer(user).data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =====================================================
# 👤 PROFILE
# =====================================================
@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user

    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)

    if request.method == "PUT":
        if "profile_picture" in request.FILES:
            user.profile_picture = request.FILES["profile_picture"]
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data)


# =====================================================
# 🛍 PRODUCT LIST + CREATE
# =====================================================
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def product_list(request):

    if request.method == "GET":
        products = Product.objects.all().order_by("-created_at")
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(vendor=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


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


# =====================================================
# ⭐ REVIEWS (RESTORED — THIS FIXES YOUR ERROR)
# =====================================================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_review(request):
    serializer = ReviewSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_review(request):
    review_id = request.data.get("review_id")
    review = get_object_or_404(Review, id=review_id, user=request.user)

    serializer = ReviewSerializer(review, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_review(request):
    review_id = request.data.get("review_id")
    review = get_object_or_404(Review, id=review_id, user=request.user)

    review.delete()
    return Response({"message": "Deleted"})


# =====================================================
# ❤️ WISHLIST
# =====================================================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    serializer = WishlistSerializer(wishlist, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_from_wishlist(request):
    product_id = request.data.get("product_id")

    item = get_object_or_404(Wishlist, user=request.user, product_id=product_id)
    item.delete()

    return Response({"message": "Removed from wishlist"})