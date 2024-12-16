from django.contrib import admin

from .models import Product, DiscountCode, Cart, CartItem, Review

admin.site.register(Product)
admin.site.register(DiscountCode)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Review)
