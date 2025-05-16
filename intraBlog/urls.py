from django.contrib import admin
from django.urls import include, path
from blog.views import PostCreateView, PostDeleteView, PostDetailView, PostListView, PostUpdateView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = (
    [
        path('i18n/', include('django.conf.urls.i18n')),
        path('', PostListView.as_view(), name='post_list'),
        path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
        path('post/create/', PostCreateView.as_view(), name='post_create'),
        path('post/<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
        path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
        path('tinymce/', include('tinymce.urls')),
    ] 
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + i18n_patterns(
        path("admin/", admin.site.urls),
    )
)