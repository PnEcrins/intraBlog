from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tiny_mce

class PostQuerySet(models.QuerySet):
    def for_user(self, user):
        if user.is_superuser:
            return self
        return self.filter(author=user)

class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def for_user(self, user):
        return self.get_queryset().for_user(user)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "categories"
        
    def __str__(self):
        return self.name

class Post(models.Model):  
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = tiny_mce.HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)
    posted = models.BooleanField(default=False)   
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)

    objects = PostManager()

    def __str__(self):
        return self.title
    


