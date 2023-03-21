from django.contrib import admin
from app_blog.models import Post, Images


@admin.register(Post)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'create_date']
    pass

@admin.register(Images)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['post', 'image']
    pass