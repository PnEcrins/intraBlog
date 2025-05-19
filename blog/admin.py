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
        return super().has_change_permission(request, obj) and (
            obj is None or obj.author == request.user
        )

    # Allow delete if superuser or if user owns the object
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return (
            super().has_delete_permission(request, obj)
            and obj is not None
            and obj.author == request.user
        )

    # Allow add if user is superuser or belongs to "Publisher" group
    def has_add_permission(self, request):
        return request.user.is_superuser or self._is_publisher(request.user)

    # Automatically assign current user as author when saving
    def save_model(self, request, obj, form, change):
        if not change or not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    # Check if user is in "Publisher" group
    def _is_publisher(self, user):
        return user.groups.filter(name=PUBLISHER_GROUP_NAME).exists()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Format category display as comma-separated list
    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])

    list_display = ("name",)
    search_fields = ("name",)

    # Only superusers can access categories module
    def has_module_permission(self, request):
        return request.user.is_superuser

    # Only superusers can view categories
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    # Only superusers can add categories
    def has_add_permission(self, request):
        return request.user.is_superuser

    # Only superusers can edit categories
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    # Only superusers can delete categories
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
