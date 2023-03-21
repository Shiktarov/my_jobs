from django.contrib import admin
from app_goods.models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['code', 'price']
