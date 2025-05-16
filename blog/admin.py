from django.contrib import admin
from django import forms
from .models import Post, Category
from tinymce.widgets import TinyMCE

PUBLISHER_GROUP_NAME = "Publisher"

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE())

    class Meta:
        model = Post
        fields = '__all__'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'posted', 'image')
    list_filter = ('author', 'posted', 'categories', 'created_at')
    search_fields = ('title', 'content')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  
        elif self._is_publisher(request.user):
            return qs.filter(posted=True) | qs.filter(author=request.user)
        else:
            return qs.none()

    def has_view_permission(self, request, obj=None):
        return True  

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if self._is_publisher(request.user):
            return obj is None or obj.author == request.user
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if self._is_publisher(request.user):
            return obj is not None and obj.author == request.user
        return False

    def has_add_permission(self, request):
        return request.user.is_superuser or self._is_publisher(request.user)

    def save_model(self, request, obj, form, change):
        if not change or not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def _is_publisher(self, user):
        return user.groups.filter(name=PUBLISHER_GROUP_NAME).exists()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])

    list_display = ('name',)
    search_fields = ('name',)

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
