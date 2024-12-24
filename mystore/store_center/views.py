from rest_framework import generics
from rest_framework import serializers
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Review, Product, Cart  # Importing the necessary models
from .serializers import ReviewSerializer, ProductSerializer, CartSerializer  # Importing the necessary serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class EmailVerificationView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully."}, status=200)
        else:
            return Response({"error": "Invalid token or user."}, status=400)

class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class LikeProductView(generics.GenericAPIView):
    """
    View to like a product.
    """
    def post(self, request, product_id):
        user = request.user  # Get the current user
        try:
            product = Product.objects.get(id=product_id)
            # Add the user to the product's likes
            product.likes.add(user)
            return Response({"message": "Product liked successfully!"}, status=200)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=404)

class ProductDetailView(generics.RetrieveAPIView):
    """
    View to retrieve a product's details.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartView(generics.ListCreateAPIView):
    """
    View to list and create carts.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class ProductListView(generics.ListAPIView):
    """
    View to list all products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class PasswordResetView(generics.GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            # Generate token and send email logic here
            return Response({"message": "Password reset email sent."}, status=200)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)
