from rest_framework import serializers
from blog.models import Post, Category

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
            'file',
            'author',        
            'author_name',   
            'categories',    
            'category_names' 
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"