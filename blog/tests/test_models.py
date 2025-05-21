from django.test import TestCase
from blog.models import Post
from blog.tests.factories import UserFactory, SuperUserFactory, PostFactory, CategoryFactory


class PostModelTestCase(TestCase):
    def setUp(self):
        # Create users
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.admin = SuperUserFactory()

        # Create posts (some posted=True, some False)
        self.user1_posts = PostFactory.create_batch(2, author=self.user1, posted=True)
        self.user1_drafts = PostFactory.create_batch(1, author=self.user1, posted=False)

        self.user2_posts = PostFactory.create_batch(2, author=self.user2, posted=True)
        self.user2_drafts = PostFactory.create_batch(1, author=self.user2, posted=False)

        self.admin_posts = PostFactory.create_batch(3, author=self.admin, posted=True)
        self.admin_drafts = PostFactory.create_batch(1, author=self.admin, posted=False)

        # Categories
        self.cat1 = CategoryFactory(name="Nature")
        self.cat2 = CategoryFactory(name="Loisir")
        self.cat3 = CategoryFactory(name="Info")
        self.cat4 = CategoryFactory(name="Event")


    def test_regular_user_sees_all_posted_posts_and_own_drafts(self):
        request = type("Request", (), {"user": self.user1})()
        queryset = Post.objects.get_authorized_posts(self.user1, request)

        # expects: 2 posted from user1 + 2 from user2 + 3 from admin = 7
        posted_posts = queryset.filter(posted=True)
        self.assertEqual(posted_posts.count(), 7)
        for post in posted_posts:
            self.assertTrue(post.posted)

        # expects: 1 own draft from user1
        own_drafts = queryset.filter(posted=False)
        self.assertEqual(own_drafts.count(), 1)
        for post in own_drafts:
            self.assertEqual(post.author, self.user1)
            self.assertFalse(post.posted)

        # total: 7 posted + 1 draft = 8 posts 
        self.assertEqual(queryset.count(), 8)


    # obvious tests - optional
    def test_post_str_returns_title(self):
        post = PostFactory(title="Hello World")
        self.assertEqual(str(post), "Hello World")


    def test_category_str_returns_name(self):
        self.assertEqual(str(self.cat1), "Nature")
        self.assertEqual(str(self.cat2), "Loisir")
        self.assertEqual(str(self.cat3), "Info")
        self.assertEqual(str(self.cat4), "Event")
