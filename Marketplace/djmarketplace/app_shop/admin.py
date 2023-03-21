from django.contrib import admin
from app_shop.models import Product, Category

@admin.register(Category)
class ShopProduct(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'created']
