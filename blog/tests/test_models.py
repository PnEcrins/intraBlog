from django.contrib.auth.models import User
from django.test import TestCase
from blog.models import Post, Category

class PostModelTestCase(TestCase):
    fixtures = ['data.json']

    def setUp(self):
        self.post1 = Post.objects.get(pk=1)
        self.post2 = Post.objects.get(pk=2)
        self.post3 = Post.objects.get(pk=3)

        self.cat_event = Category.objects.get(pk=1)
        self.cat_loisir = Category.objects.get(pk=2)
        self.cat_info = Category.objects.get(pk=3)

        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.admin = User.objects.get(pk=3)

    def test_post_str(self):
        self.assertEqual(str(self.post1), "titre 1")
        self.assertEqual(str(self.post2), "titre 2")
        self.assertEqual(str(self.post3), "titre 3")

    def test_post_authors(self):
        self.assertEqual(self.post1.author, self.user1)
        self.assertEqual(self.post2.author, self.user2)

    def test_post_categories(self):
        self.assertIn(self.cat_event, self.post1.categories.all())
        self.assertIn(self.cat_loisir, self.post2.categories.all())
        self.assertIn(self.cat_info, self.post3.categories.all())

    def test_post_posted_flag(self):
        self.assertTrue(self.post1.posted)
        self.assertTrue(self.post2.posted)
        self.assertTrue(self.post3.posted)

    def test_filter_posts_by_user(self):
        posts_by_user1 = Post.objects.filter(author=self.user1)
        self.assertIn(self.post1, posts_by_user1)
        self.assertIn(self.post3, posts_by_user1)
        self.assertNotIn(self.post2, posts_by_user1)

    def test_filter_by_category(self):
        event_posts = Post.objects.filter(categories=self.cat_event)
        self.assertIn(self.post1, event_posts)
        self.assertNotIn(self.post2, event_posts)

    def test_created_at_order(self):
        posts = Post.objects.order_by('created_at')
        self.assertEqual(list(posts), [self.post1, self.post2, self.post3])
