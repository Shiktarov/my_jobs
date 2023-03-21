from django.contrib import admin
from app_news.models import News, Comments, Category


class NewsAndCommentInLine(admin.TabularInline):
    model = Comments


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['name', 'create_date', 'edit_date', 'is_active', 'cat']
    list_filter = ['is_active', 'cat']
    inlines = [NewsAndCommentInLine]

    actions = ['mark_status_active', 'mark_status_noactive']

    def mark_status_active(self, request, queryset):
        queryset.update(is_active='A')

    def mark_status_noactive(self, request, queryset):
        queryset.update(is_active='N')

    mark_status_active.short_description = 'Перевести в статус Одобрено'
    mark_status_noactive.short_description = 'Перевести в статус Неактивно'

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['user_name','comment', 'user_news', 'user']
    list_filter = ['user_name', 'user_news']

    actions = ['delete_by_admin']
    def delete_by_admin(self, request, queryset):
        queryset.update(comment='Удалено администратором')

    delete_by_admin.short_description = 'Удалить текст комментариев'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
