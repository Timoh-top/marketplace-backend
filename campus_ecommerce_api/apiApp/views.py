from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView

from .models import (
    Product,
    Category,
    Cart,
    CartItem,
    Review,
    Wishlist
)

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
        user.profile_picture = request.FILES.get("profile_picture")
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data)


# =====================================================
# 🛍 PRODUCT LIST + CREATE
# =====================================================
@api_view(["GET", "POST"])
def product_list(request):

    # ---------------------
    # GET PRODUCTS
    # ---------------------
    if request.method == "GET":
        products = Product.objects.all().order_by("-created_at")
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # ---------------------
    # CREATE PRODUCT
    # ---------------------
    if request.method == "POST":
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(vendor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =====================================================
# 🛍 PRODUCT DETAIL (GET / UPDATE / DELETE)
# =====================================================
@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, id):

    product = get_object_or_404(Product, id=id)

    # ---------------------
    # GET
    # ---------------------
    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    # ---------------------
    # UPDATE
    # ---------------------
    if request.method == "PUT":

        if not request.user.is_authenticated or product.vendor != request.user:
            return Response(
                {"error": "Not allowed"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ---------------------
    # DELETE
    # ---------------------
    if request.method == "DELETE":

        if not request.user.is_authenticated or product.vendor != request.user:
            return Response(
                {"error": "Not allowed"},
                status=status.HTTP_403_FORBIDDEN
            )

        product.delete()
        return Response({"message": "Product deleted"}, status=status.HTTP_200_OK)

# =====================================================
# 🗑 DELETE PRODUCT (OWNER ONLY)
# =====================================================
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)

    # 🔒 ONLY OWNER CAN DELETE
    if product.vendor != request.user:
        return Response(
            {"error": "You are not allowed to delete this product"},
            status=403
        )

    product.delete()

    return Response(
        {"message": "Product deleted successfully"},
        status=200
    )
# =====================================================
# 📂 CATEGORIES
# =====================================================
@api_view(["GET"])
@permission_classes([AllowAny])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    serializer = CategorySerializer(category)
    return Response(serializer.data)


# =====================================================
# 🛒 CART
# =====================================================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get("product_id")
    quantity = int(request.data.get("quantity", 1))

    product = get_object_or_404(Product, id=product_id)

    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    item.quantity = item.quantity + quantity if not created else quantity
    item.save()

    return Response({"message": "Added to cart"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_cartitem_quantity(request):
    item_id = request.data.get("item_id")
    quantity = int(request.data.get("quantity", 1))

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.quantity = quantity
    item.save()

    return Response({"message": "Cart updated"})


# =====================================================
# ⭐ REVIEWS
# =====================================================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_review(request):
    serializer = ReviewSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_review(request):
    review_id = request.data.get("review_id")
    review = get_object_or_404(Review, id=review_id, user=request.user)

    serializer = ReviewSerializer(review, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    item = get_object_or_404(
        Wishlist,
        user=request.user,
        product_id=product_id
    )
    item.delete()

    return Response({"message": "Removed from wishlist"})