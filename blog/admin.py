from django.contrib import admin
from .models import Category, Post
from tinymce.widgets import TinyMCE

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'author', 'created_at', 'get_categories', 'posted', 'image')
    list_filter = ('author', 'categories', 'created_at')
    search_fields = ('title', 'content')

    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])
    get_categories.short_description = 'Categories'

    class Meta:
        widgets = {
            "content": TinyMCE()
        }


