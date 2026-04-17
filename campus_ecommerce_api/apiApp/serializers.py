from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Avg

from .models import (
    Product,
    Category,
    Review,
    Cart,
    CartItem,
    Wishlist
)

User = get_user_model()


# =====================================================
# 👤 USER SERIALIZER
# =====================================================
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "role",
            "profile_picture",
            "is_verified",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)

        if password:
            user.set_password(password)

        user.save()
        return user


# =====================================================
# 📂 CATEGORY SERIALIZER
# =====================================================
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


# =====================================================
# ⭐ REVIEW SERIALIZER
# =====================================================
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "product",
            "user",
            "rating",
            "review",
            "created_at"
        ]
        read_only_fields = ["user", "created_at"]


# =====================================================
# 🛍 PRODUCT SERIALIZER (OPTIMIZED)
# =====================================================
class ProductSerializer(serializers.ModelSerializer):
    vendor = serializers.StringRelatedField(read_only=True)

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="slug"
    )

    category_name = serializers.CharField(source="category.name", read_only=True)

    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "image",
            "slug",
            "category",        # 👈 now slug-based
            "category_name",
            "vendor",
            "is_available",
            "created_at",
            "average_rating",
            "total_reviews",
        ]

    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(avg=Avg("rating"))["avg"]
        return round(avg, 1) if avg else 0

    def get_total_reviews(self, obj):
        return obj.reviews.count()


# =====================================================
# 🛒 CART ITEM SERIALIZER
# =====================================================
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]


# =====================================================
# 🛒 CART SERIALIZER
# =====================================================
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "created_at"]


# =====================================================
# ❤️ WISHLIST SERIALIZER
# =====================================================
class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "product"]