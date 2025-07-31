from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tiny_mce
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class PostManager(models.Manager):

    def get_authorized_posts(self, request):
        if request.user.is_superuser or request.user.has_perm("blog.can_view_all_posts"):
            return super().get_queryset()
        return self.filter(author=request.user)

class Category(models.Model):
    name = models.CharField(verbose_name="Categorie", max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.name


class Post(models.Model):
    class Meta:
        permissions = [
            ("can_view_all_posts", "Can view all posts")
        ]
        ordering = ["updated_at"]

    title = models.CharField(verbose_name="Titre", max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")
    content = tiny_mce.HTMLField(verbose_name="Contenu", blank=True)
    created_at = models.DateTimeField(verbose_name="Créé le", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Éditer le", auto_now=True)
    categories = models.ManyToManyField(Category, verbose_name="Catégorie")
    posted = models.BooleanField(default=False, verbose_name="Publié")
    image = models.ImageField(
        upload_to="post_images/", null=True, blank=True, verbose_name="Image"
    )
    file = models.FileField(
        upload_to="post_files/", null=True, blank=True, verbose_name="Fichier"
    )

    objects = PostManager()

    def __str__(self):
        return self.title
