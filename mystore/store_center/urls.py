from django.urls import path, include

from .views import UserRegistrationView, EmailVerificationView, ReviewListView, LikeProductView, ProductListView, ProductDetailView, CartView

urlpatterns = [  
    path('email-verify/<uidb64>/<token>/', EmailVerificationView.as_view(), name='email_verify'),  # Add the email verification URL
    path('register/', UserRegistrationView.as_view(), name='register'),  # User registration
    path('verify-email/<int:user_id>/', EmailVerificationView.as_view(), name='verify_email'),  # Email verification
    path('products/', ProductListView.as_view(), name='product_list'),  # List all products
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),  # Product detail
    path('cart/', CartView.as_view(), name='cart'),  # User's cart
    path('like-product/<int:product_id>/', LikeProductView.as_view(), name='like_product'),  # Like a product
]
