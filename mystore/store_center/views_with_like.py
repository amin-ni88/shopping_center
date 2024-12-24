from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserSerializer, ProductSerializer
from rest_framework.views import APIView
import logging
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

logger = logging.getLogger(__name__)

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info(f"User registered: {user.username}")
=======

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
=======
class EmailVerificationView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, verification_token):
        user = get_object_or_404(User, verification_token=verification_token)
        user.is_verified = True
        user.save()
        logger.info(f"Email verified for user: {user.username}")
        return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)

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
        return Product.objects.all()

class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer

    def get_object(self):
        return self.get_queryset().get(pk=self.kwargs['pk'])

class LikeProductView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, product_id):
        logger.info(f"Product {product_id} liked.")
        return Response({"message": f"Product {product_id} liked successfully."}, status=status.HTTP_200_OK)

# Additional views for cart and checkout can be added here
