from django.contrib import admin

# Register your models here.

from .models import Category, Event


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'price',
        'is_active',
        'views_count',
        'created_at',
    )
    list_filter = ('is_active', 'categories')
    search_fields = ('title', 'description')
    list_select_related = ('author',)
    filter_horizontal = ('categories', 'participants')
