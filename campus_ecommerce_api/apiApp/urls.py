from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

    # =====================================================
    # 🛍 PRODUCTS
    # =====================================================
    path('products/', views.product_list),
    path('products/<int:id>/', views.product_detail),
    path('products/create/', views.create_product),

    # =====================================================
    # 📂 CATEGORIES
    # =====================================================
    path('categories/', views.category_list),
    path('categories/<slug:slug>/', views.category_detail),

    # =====================================================
    # 🛒 CART
    # =====================================================
    path('add_to_cart/', views.add_to_cart),
    path('update_cartitem_quantity/', views.update_cartitem_quantity),
    path('cart/<str:cart_code>/', views.get_cart),

    # =====================================================
    # ⭐ REVIEWS
    # =====================================================
    path('add_review/', views.add_review),
    path('update_review/', views.update_review),
    path('delete_review/', views.delete_review),

    # =====================================================
    # ❤️ WISHLIST
    # =====================================================
    path('get_wishlist/', views.get_wishlist),
    path('delete_from_wishlist/', views.delete_from_wishlist),

    # =====================================================
    # 👤 AUTH
    # =====================================================
    path('register/', views.register_user),
    path('profile/', views.get_profile),

    path('login/', views.MyTokenView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]