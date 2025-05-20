from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Post, Category
from rest_framework.test import APIClient
from datetime import datetime

class PostAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username="test_user", password="test_pwd")
        self.category = Category.objects.create(name="Test_Category")

        Post.objects.create(
            title="Public Post",
            author=self.user,
            content="Content 1",
            created_at=datetime(2025, 5, 19),
            posted=True,
        ).categories.add(self.category)

        Post.objects.create(
            title="Private Post",
            author=self.user,
            content="Content 2",
            created_at=datetime(2025, 5, 20),
            posted=False
        ).categories.add(self.category)

    def test_only_posted_visible(self):
        response = self.client.get("/api/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['title'], "Public Post")

    def test_filter_by_category(self):
        response = self.client.get(f"/api/posts/?category={self.category.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_limit_results(self):
        response = self.client.get("/api/posts/?limit=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
