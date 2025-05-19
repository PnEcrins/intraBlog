from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tiny_mce
from django.utils.translation import gettext_lazy as _

class PostManager(models.Manager):

    def get_authorized_posts(self, user, request):
        if request.user.is_superuser:
            return super().get_queryset()
        return self.all().filter(author__id=request.user.id)

class Category(models.Model):
    name = models.CharField(_('Category'), max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "categories"
        
    def __str__(self):
        return self.name

class Post(models.Model):  
    title = models.CharField(_('Title'), max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = tiny_mce.HTMLField(_('Content'), blank=True)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)
    categories = models.ManyToManyField(Category)
    posted = models.BooleanField(default=False)   
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    
    objects = PostManager()

    def __str__(self):
        return self.title
    


