from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserSerializer, ProductSerializer
import logging
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"User registered: {user.username}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailVerificationView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, verification_token):
        try:
            user = User.objects.get(verification_token=verification_token)
            user.is_verified = True
            user.save()
            logger.info(f"Email verified for user: {user.username}")
            return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.warning("Invalid verification token used.")
            return Response({"error": "Invalid verification token."}, status=status.HTTP_400_BAD_REQUEST)

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Logic to retrieve products
        return Product.objects.all()

class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer

    def get_object(self):
        # Logic to retrieve a specific product
        return self.get_queryset().get(pk=self.kwargs['pk'])

# Additional views for cart and checkout can be added here
