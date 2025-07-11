from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tiny_mce
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class PostManager(models.Manager):

    def get_authorized_posts(self, user, request):
        if request.user.is_superuser:
            return super().get_queryset()
        return self.filter(posted=True) | self.filter(author=user, posted=False)


class Category(models.Model):
    name = models.CharField(verbose_name=_("Category"), max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Author"))
    content = tiny_mce.HTMLField(verbose_name=_("Content"), blank=True)
    created_at = models.DateTimeField(verbose_name=_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated_at"), auto_now=True)
    categories = models.ManyToManyField(Category, verbose_name=_("Category"))
    posted = models.BooleanField(default=False, verbose_name=_("Posted"))
    image = models.ImageField(
        upload_to="post_images/", null=True, blank=True, verbose_name=_("Image")
    )
    file = models.FileField(
        upload_to="post_files/", null=True, blank=True, verbose_name=_("File")
    )

    objects = PostManager()

    def __str__(self):
        return self.title
