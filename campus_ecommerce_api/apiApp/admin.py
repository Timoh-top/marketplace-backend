from django.contrib import admin
from .models import CustomUser, Category, Product, Review, Cart, CartItem, Wishlist


# =========================
# USER
# =========================
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "role", "is_active")
    search_fields = ("username", "email")
    list_filter = ("role", "is_active")


# =========================
# CATEGORY
# =========================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


# =========================
# PRODUCT
# =========================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category", "vendor", "is_available")
    search_fields = ("name",)
    list_filter = ("category", "is_available")
    prepopulated_fields = {"slug": ("name",)}


# =========================
# REVIEW
# =========================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "user", "rating", "created_at")
    list_filter = ("rating",)


# =========================
# CART
# =========================
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")


# =========================
# CART ITEM
# =========================
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity")


# =========================
# WISHLIST
# =========================
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product")