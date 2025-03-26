from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
     list_display = ['id', 'user__id', 'user']
     list_display_links = ['id', 'user__id', 'user']



@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
     list_display = ['id', 'cart', 'book', 'quantity', 'total_price', 'created_at', 'updated_at', 'status', 'is_active']
     list_display_links = ['id', 'book', 'quantity',]
     search_fields = ['cart', 'book', 'created_at', 'status']
     list_editable = ('status', 'is_active')