from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

    # =====================================================
    # 🔐 AUTH
    # =====================================================
    path('register/', views.register_user, name="register"),
    path('login/', views.MyTokenView.as_view(), name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),

    # =====================================================
    # 👤 PROFILE
    # =====================================================
    path('profile/', views.get_profile, name="profile"),

    # =====================================================
    # 🛍 PRODUCTS
    # =====================================================
    path('products/', views.product_list, name="product-list"),  
    path('products/<int:id>/', views.product_detail, name="product-detail"),


    # =====================================================
    # 📂 CATEGORIES
    # =====================================================
    path('categories/', views.category_list, name="category-list"),
    path('categories/<slug:slug>/', views.category_detail, name="category-detail"),

    # =====================================================
    # 🛒 CART
    # =====================================================
    path('cart/', views.get_cart, name="cart"),
    path('cart/add/', views.add_to_cart, name="add-to-cart"),
    path('cart/update/', views.update_cartitem_quantity, name="update-cart"),

    # =====================================================
    # ⭐ REVIEWS
    # =====================================================
    path('reviews/add/', views.add_review, name="add-review"),
    path('reviews/update/', views.update_review, name="update-review"),
    path('reviews/delete/', views.delete_review, name="delete-review"),

    # =====================================================
    # ❤️ WISHLIST
    # =====================================================
    path('wishlist/', views.get_wishlist, name="wishlist"),
    path('wishlist/delete/', views.delete_from_wishlist, name="wishlist-delete"),
]