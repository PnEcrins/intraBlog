from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from blog.models import Post, Category


class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="test_pwd")
        self.category = Category.objects.create(name="Test_Category")

        self.post1 = Post.objects.create(
            title="Post 1",
            author=self.user,
            content="Content 1",
            created_at=datetime(2025, 5, 19),
            posted=True,
        )
        self.post1.categories.add(self.category)

        self.post2 = Post.objects.create(
            title="Post 2",
            author=self.user,
            content="Content 2",
            created_at=datetime(2025, 5, 20),
            posted=False
        )
        self.post2.categories.add(self.category)

    def test_post_str_returns_title(self):
        self.assertEqual(str(self.post1), "Post 1")
        self.assertEqual(str(self.post2), "Post 2")

    def test_category_str_returns_name(self):
        self.assertEqual(str(self.category), "Test_Category")

    def test_post_category_relationship(self):
        self.assertIn(self.category, self.post1.categories.all())
        self.assertIn(self.category, self.post2.categories.all())

    def test_post_filter_posted_true(self):
        posted_posts = Post.objects.filter(posted=True)
        self.assertEqual(len(posted_posts), 1)
        self.assertEqual(posted_posts[0].title, "Post 1")

    def test_post_filter_posted_false(self):
        private_posts = Post.objects.filter(posted=False)
        self.assertEqual(len(private_posts), 1)
        self.assertEqual(private_posts[0].title, "Post 2")

    def test_post_author(self):
        self.assertEqual(self.post1.author.username, "test_user")
