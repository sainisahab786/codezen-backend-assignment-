from django.contrib import admin
from .models import Customer, Seller, Product, Order, PlatformApiCall

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'user')
    search_fields = ('name', 'mobile', 'user__username')

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'user')
    search_fields = ('name', 'mobile', 'user__username')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount')
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'seller', 'amount')
    list_filter = ('customer', 'seller')
    search_fields = ('customer__name', 'seller__name', 'products__name')
    filter_horizontal = ('products',)

@admin.register(PlatformApiCall)
class PlatformApiCallAdmin(admin.ModelAdmin):
    list_display = ('user', 'requested_url', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('user__username', 'requested_url')