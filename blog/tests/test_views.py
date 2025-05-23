from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch
from blog.tests.factories import UserFactory, SuperUserFactory, PostFactory, CategoryFactory
from intraBlog.settings import MAX_QUERY_LIMIT

class PostAPITestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()

        # Create users
        cls.user1 = UserFactory()
        cls.user2 = UserFactory()
        cls.admin = SuperUserFactory()

        # Categories
        cls.cat1 = CategoryFactory(name="Nature")
        cls.cat2 = CategoryFactory(name="Loisir")
        cls.cat3 = CategoryFactory(name="Info")
        cls.cat4 = CategoryFactory(name="Event")

        # Create posts
        cls.user1_posts = PostFactory.create_batch(2, author=cls.user1, posted=True, categories=[cls.cat1])
        cls.user1_drafts = PostFactory.create_batch(1, author=cls.user1, posted=False, categories=[cls.cat1])

        cls.user2_posts = PostFactory.create_batch(2, author=cls.user2, posted=True, categories=[cls.cat2])
        cls.user2_drafts = PostFactory.create_batch(1, author=cls.user2, posted=False, categories=[cls.cat2])

        cls.admin_posts = PostFactory.create_batch(3, author=cls.admin, posted=True, categories=[cls.cat1])
        cls.admin_drafts = PostFactory.create_batch(1, author=cls.admin, posted=False, categories=[cls.cat2])

    def test_only_posted_visible_for_anonymous(self):
        response = self.client.get("/api/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)
        for post in response.json()["results"]:
            self.assertTrue(post["posted"])

    def test_filter_by_category(self):
        response = self.client.get(f"/api/posts/?category={self.cat1.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)
        for post in response.json()["results"]:
            self.assertIn("Nature", post["category_names"])

    def test_filter_by_author(self):
        response = self.client.get(f"/api/posts/?author={self.user1.id}")
        self.assertEqual(response.status_code, 200)
        # The response is paginated, so posts are in response.json()["results"]
        for post in response.json()["results"]:
            self.assertEqual(post["author"], self.user1.id)

    def test_limit_results(self):
        response = self.client.get("/api/posts/?limit=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)

    # Error handling tests

    def test_invalid_category_id(self):
        response = self.client.get("/api/posts/?category=abc")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Category ID must be a number.", str(response.content))

    def test_invalid_author_id(self):
        response = self.client.get("/api/posts/?author=notanumber")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Author ID must be a number.", str(response.content))

    def test_invalid_limit(self):
        response = self.client.get("/api/posts/?limit=notanumber")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Limit must be an integer.", str(response.content))

    def test_limit_exceeds_max(self):
        response = self.client.get(f"/api/posts/?limit={MAX_QUERY_LIMIT + 1}")
        self.assertEqual(response.status_code, 403)
        self.assertIn(f"limit has to be between 0 and {MAX_QUERY_LIMIT}.", str(response.content))

    def test_invalid_date_format(self):
        response = self.client.get("/api/posts/?date=2023-99-99")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid date format. Use YYYY-MM-DD.", str(response.content))

    # Test to force an unexpected error
    def test_unexpected_error_handling(self):
        # Patch Post.objects.filter to raise a RuntimeError
        with patch("blog.views.Post.objects.filter", side_effect=RuntimeError("DB error")):
            response = self.client.get("/api/posts/")
            self.assertEqual(response.status_code, 400)
            self.assertIn("An unexpected error occurred:", response.json()[0])  