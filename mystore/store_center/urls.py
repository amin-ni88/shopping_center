from django.urls import path

from .views import UserRegistrationView, EmailVerificationView, ProductListView, ProductDetailView, CartView, \
    CartItemView, CheckoutView, ReviewListView, LikeProductView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify-email/<int:user_id>/', EmailVerificationView.as_view(), name='verify_email'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart-item/<int:pk>/', CartItemView.as_view(), name='cart_item'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('reviews/', ReviewListView.as_view(), name='review_list'),
    path('like-product/<int:product_id>/', LikeProductView.as_view(), name='like_product'),
]
