# store/views.py

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from .models import Product, Cart, Review, CartItem
from .serializers import UserRegistrationSerializer, ProductSerializer, CartSerializer, \
    ReviewSerializer, CartItemSerializer

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Send verification email
        verification_link = request.build_absolute_uri(
            reverse('verify_email', kwargs={'user_id': user.id})
        )
        send_mail(
            'Verify your email',
            f'Click the link to verify your email: {verification_link}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EmailVerificationView(generics.GenericAPIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
        return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = serializer.save(user=request.user)
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


class CartItemView(generics.UpdateAPIView):
    serializer_class = CartItemSerializer

    def get_object(self):
        cart_item = CartItem.objects.get(id=self.kwargs['pk'])
        return cart_item

    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        serializer = self.get_serializer(cart_item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CheckoutView(generics.GenericAPIView):
    def post(self, request):
        # Implement payment processing with Stripe here
        return Response({"message": "Payment processed successfully."}, status=status.HTTP_200_OK)


class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeProductView(generics.GenericAPIView):
    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        user = request.user
        if user in product.likes.all():
            product.likes.remove(user)
            return Response({"message": "Product unliked."}, status=status.HTTP_200_OK)
        else:
            product.likes.add(user)
            return Response({"message": "Product liked."}, status=status.HTTP_200_OK)
