from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.text import slugify
from django.conf import settings
from django.db.models import Avg
import uuid

from cloudinary.models import CloudinaryField


# =====================================================
# 👤 USER MANAGER
# =====================================================
class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        username = extra_fields.pop("username", email.split("@")[0])

        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)


# =====================================================
# 👤 USER MODEL
# =====================================================
class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=[("buyer", "Buyer"), ("vendor", "Vendor")],
        default="buyer"
    )

    # ✔ Cloudinary FIX
    profile_picture = CloudinaryField('image', blank=True, null=True)

    is_verified = models.BooleanField(default=False)

    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# =====================================================
# 📦 CATEGORY
# =====================================================
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = base_slug
            counter = 1

            while Category.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}-{uuid.uuid4().hex[:4]}"
                counter += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =====================================================
# 🛍 PRODUCT (CLOUDINARY FIXED)
# =====================================================
class Product(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # ✔ Cloudinary FIX
    image = CloudinaryField('image', blank=True, null=True)

    slug = models.SlugField(unique=True, blank=True)

    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        related_name="products"
    )

    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products"
    )

    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # ✔ Slug generator
    def generate_unique_slug(self):
        base_slug = slugify(self.name)
        unique_slug = base_slug
        counter = 1

        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{counter}-{uuid.uuid4().hex[:5]}"
            counter += 1

        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()

        super().save(*args, **kwargs)

    # ✔ Safe rating
    def average_rating(self):
        return self.reviews.aggregate(avg=Avg("rating"))["avg"] or 0

    def __str__(self):
        return self.name


# =====================================================
# ⭐ REVIEW (FIXED — ADDED created_at)
# =====================================================
class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    rating = models.PositiveIntegerField()
    review = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)  # ✔ FIXED

    class Meta:
        unique_together = ("product", "user")

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"


# =====================================================
# 🛒 CART
# =====================================================
class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}'s cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


# =====================================================
# ❤️ WISHLIST
# =====================================================
class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.email} -> {self.product.name}"