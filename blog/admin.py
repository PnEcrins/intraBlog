from django.contrib import admin
from django import forms
from .models import Post, Category
from tinymce.widgets import TinyMCE

PUBLISHER_GROUP_NAME = "Publisher"


# Custom form using TinyMCE for the content field
class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE())

    class Meta:
        model = Post
        fields = "__all__"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "posted", "image")
    list_filter = ("author", "posted", "categories", "created_at")
    search_fields = ("title", "content")

    # Hide 'author' field for non-superusers
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            return [f for f in fields if f != "author"]
        return fields

    # Show all posted posts + user’s own posted and not posted posts
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(posted=True) | qs.filter(author=request.user)

    # Allow change if superuser or if user owns the object
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.author == request.user:
            return True
        return False

    # Allow delete if superuser or if user owns the object
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.author == request.user:
            return True
        return False  

    # Automatically assign current user as author when saving
    def save_model(self, request, obj, form, change):
        if not change or not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)
        

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Format category display as comma-separated list
    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])

    list_display = ("name",)
    search_fields = ("name",)