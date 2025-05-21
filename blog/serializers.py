from rest_framework import serializers
from blog.models import Post, Category
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    category_names = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
        source='categories'
    )

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'created_at',
            'updated_at',
            'posted',
            'image',
            'author',        
            'author_name',   
            'categories',    
            'category_names' 
        ]