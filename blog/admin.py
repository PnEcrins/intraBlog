from django.contrib import admin
from .models import Category, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('categories', 'created_at', 'author')
    date_hierarchy = 'created_at'
    autocomplete_fields = ['author', 'categories']
