from math import e
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.filters import OrderingFilter

from .models import Category, Post
from rest_framework import viewsets
from .serializers import CategorySerializer, PostSerializer
from intraBlog.settings import MAX_QUERY_LIMIT


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    filter_backends = [OrderingFilter]
    def get_queryset(self):
        try:
            # Only published posts, sorted newest first
            queryset = Post.objects.filter(posted=True)

            # Filter by category ID
            category = self.request.query_params.get("categories")

            # convert to array if more than 1 category is provided
            if category and "," in category:
                category_ids = category.split(",")
                if not all(cat_id.isdigit() for cat_id in category_ids):
                    raise ValidationError("All category IDs must be numbers.")
                category_ids = [int(cat_id) for cat_id in category_ids]
                queryset = queryset.filter(categories__id__in=category_ids).distinct()
            else:
                # If a single category is provided, ensure it's a number
                if category:
                    if not category.isdigit():
                        raise ValidationError("Category ID must be a number.")
                    queryset = queryset.filter(categories__id=int(category))

            # Filter by author ID
            user_id = self.request.query_params.get("author")
            if user_id:
                if not user_id.isdigit():
                    raise ValidationError("Author ID must be a number.")
                queryset = queryset.filter(author__id=int(user_id))

            # Filter by creation date (YYYY-MM-DD)
            date = self.request.query_params.get("date")
            if date:
                try:
                    queryset = queryset.filter(created_at__date=date)
                except (ValueError, DjangoValidationError):
                    raise ValidationError("Invalid date format. Use YYYY-MM-DD.")

            # Limit the number of results
            limit = self.request.query_params.get("limit")
            if limit:
                if not limit.isdigit():
                    raise ValidationError("Limit must be an integer.")
                limit_int = int(limit)
                if limit_int > MAX_QUERY_LIMIT or limit_int <= 0:
                    raise PermissionDenied(f"limit has to be between 0 and {MAX_QUERY_LIMIT}.")
                queryset = queryset[:limit_int]

            return queryset

        except (ValidationError, PermissionDenied) as e:
            raise e  # Let DRF handle known API errors
        except Exception as e:
            # Fallback for unexpected exceptions
            raise ValidationError(f"An unexpected error occurred: {str(e)}")

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by("id")