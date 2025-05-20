from rest_framework.exceptions import PermissionDenied, ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Post
from rest_framework import viewsets
from .serializers import PostSerializer
from intraBlog.settings import MAX_QUERY_LIMIT


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        try:
            # Only published posts, sorted newest first
            queryset = Post.objects.filter(posted=True).order_by("-created_at")

            # Filter by category ID
            category = self.request.query_params.get("category")
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
                if limit_int > MAX_QUERY_LIMIT:
                    raise PermissionDenied(f"Maximum limit is {MAX_QUERY_LIMIT}.")
                queryset = queryset[:limit_int]

            return queryset

        except (ValidationError, PermissionDenied) as e:
            raise e  # Let DRF handle known API errors
        except Exception as e:
            # Fallback for unexpected exceptions
            raise ValidationError(f"An unexpected error occurred: {str(e)}")