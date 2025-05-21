from django.test import TestCase
from rest_framework.test import APIClient
from blog.tests.factories import UserFactory, SuperUserFactory, PostFactory, CategoryFactory


class PostAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create users
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.admin = SuperUserFactory()

        # Categories
        self.cat1 = CategoryFactory(name="Nature")
        self.cat2 = CategoryFactory(name="Loisir")
        self.cat3 = CategoryFactory(name="Info")
        self.cat4 = CategoryFactory(name="Event")

        # Create posts
        self.user1_posts = PostFactory.create_batch(2, author=self.user1, posted=True, categories=[self.cat1])
        self.user1_drafts = PostFactory.create_batch(1, author=self.user1, posted=False, categories=[self.cat1])

        self.user2_posts = PostFactory.create_batch(2, author=self.user2, posted=True, categories=[self.cat2])
        self.user2_drafts = PostFactory.create_batch(1, author=self.user2, posted=False, categories=[self.cat2])

        self.admin_posts = PostFactory.create_batch(3, author=self.admin, posted=True, categories=[self.cat1])
        self.admin_drafts = PostFactory.create_batch(1, author=self.admin, posted=False, categories=[self.cat2])


    def test_only_posted_visible_for_anonymous(self):
        response = self.client.get("/api/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 7)  # 2+2+3 posted
        for post in response.json():
            self.assertTrue(post["posted"])


    def test_filter_by_category(self):
        response = self.client.get(f"/api/posts/?category={self.cat1.id}")
        self.assertEqual(response.status_code, 200)
        # 2 from user1 + 3 from admin in cat1 and posted
        self.assertEqual(len(response.json()), 5)
        for post in response.json():
            self.assertIn("Nature", post["category_names"])


    def test_limit_results(self):
        response = self.client.get("/api/posts/?limit=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
