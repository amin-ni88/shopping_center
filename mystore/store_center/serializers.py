from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Product, DiscountCode, Cart, CartItem, Review

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def get_likes_count(self, obj):
        return obj.likes.count()


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['user', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        cart = Cart.objects.create(**validated_data)
        for item_data in items_data:
            CartItem.objects.create(cart=cart, **item_data)
        return cart


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['product', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']
