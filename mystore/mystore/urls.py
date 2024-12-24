from django.contrib import admin
from django.urls import path, include
from store_center.views import PasswordResetView  # Import the password reset view
from store_center.views import UserRegistrationView  # Import the registration view
from store_center.views import EmailVerificationView  # Import other views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('store_center.urls')),  # Added versioning
    path('accounts/', include('django.contrib.auth.urls')),  # Include auth URLs for password reset
    path('api/v1/password-reset/', PasswordResetView.as_view(), name='password_reset_api'),  # Add password reset API
    path('api/v1/register/', UserRegistrationView.as_view(), name='user_registration'),  # Add user registration API
]
