from django.contrib import admin
from django.urls import include, path
from blog.views import (
    CategoryViewSet,
    PostViewSet,
)
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("posts", PostViewSet, "post")
router.register("categories", CategoryViewSet, "category")

urlpatterns = (
    [
        path("i18n/", include("django.conf.urls.i18n")),
        path("api/", include(router.urls)),
        path("tinymce/", include("tinymce.urls")),
        path("", admin.site.urls),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
