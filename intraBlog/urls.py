from django.contrib import admin
from django.urls import include, path
from blog.views import (
    PostViewSet,
)
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("posts", PostViewSet, "post")

urlpatterns = (
    [
        path("i18n/", include("django.conf.urls.i18n")),
        path("api/", include(router.urls)),
        path("tinymce/", include("tinymce.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + i18n_patterns(
        path("admin/", admin.site.urls),
    )
)