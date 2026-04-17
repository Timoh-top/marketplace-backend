from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import add_review


urlpatterns = [

    # =====================================================
    # 🛍 PRODUCTS (FIXED: ID BASED)
    # =====================================================
    path('products/', views.product_list, name='product_list'),
    path('products/<int:id>/', views.product_detail, name='product_detail'),
    path("products/<int:id>/delete/", views.delete_product, name="delete_product"),
      # ✅ FIXED

    # =====================================================
    # 📂 CATEGORIES
    # =====================================================
    path('categories/', views.category_list, name='category_list'),
    path('categories/<slug:slug>/', views.category_detail, name='category_detail'),

    # =====================================================
    # 🛒 CART
    # =====================================================
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('update_cartitem_quantity/', views.update_cartitem_quantity, name='update_cartitem_quantity'),
    path('cart/<str:cart_code>/', views.get_cart, name='get_cart'),

    # =====================================================
    # ⭐ REVIEWS
    # =====================================================
    path('add_review/', views.add_review, name='add_review'),
    path('update_review/', views.update_review, name='update_review'),
    path('delete_review/', views.delete_review, name='delete_review'),

    # =====================================================
    # ❤️ WISHLIST
    # =====================================================
    path('get_wishlist/', views.get_wishlist, name='get_wishlist'),
    path('delete_from_wishlist/', views.delete_from_wishlist, name='delete_from_wishlist'),

    # =====================================================
    # 👤 USER AUTH
    # =====================================================
    path('register/', views.register_user, name='register_user'),
    path('profile/', views.get_profile, name='get_profile'),

    # =====================================================
    # 🔐 AUTH
    # =====================================================
    path('login/', views.MyTokenView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # =====================================================
    # 📝 POSTS (MARKETPLACE SYSTEM)
    # =====================================================
]