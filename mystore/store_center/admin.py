from django.contrib import admin

from .models import Product, DiscountCode, Cart, CartItem, Review

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name',)
    list_filter = ('price',)

class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Removed created_at since it doesn't exist in the Cart model
    search_fields = ('user__username',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username')

admin.site.register(Product, ProductAdmin)
admin.site.register(DiscountCode)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Review, ReviewAdmin)
