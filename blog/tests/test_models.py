from django.test import TestCase
from blog.models import Post
from blog.tests.factories import UserFactory, SuperUserFactory, PostFactory, CategoryFactory


class PostModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create users
        cls.user1 = UserFactory()
        cls.user2 = UserFactory()
        cls.admin = SuperUserFactory()

        # Create posts (some posted=True, some False)
        cls.user1_posts = PostFactory.create_batch(2, author=cls.user1, posted=True)
        cls.user1_drafts = PostFactory.create_batch(1, author=cls.user1, posted=False)

        cls.user2_posts = PostFactory.create_batch(2, author=cls.user2, posted=True)
        cls.user2_drafts = PostFactory.create_batch(1, author=cls.user2, posted=False)

        cls.admin_posts = PostFactory.create_batch(3, author=cls.admin, posted=True)
        cls.admin_drafts = PostFactory.create_batch(1, author=cls.admin, posted=False)

        # Categories
        cls.cat1 = CategoryFactory(name="Nature")
        cls.cat2 = CategoryFactory(name="Loisir")
        cls.cat3 = CategoryFactory(name="Info")
        cls.cat4 = CategoryFactory(name="Event")


    def test_superuser_sees_all_posts(self):
        request = type("Request", (), {"user": self.admin})()
        queryset = Post.objects.get_authorized_posts(request)
        # All posts should be visible to superuser
        total_posts = (
            len(self.user1_posts) + len(self.user1_drafts) +
            len(self.user2_posts) + len(self.user2_drafts) +
            len(self.admin_posts) + len(self.admin_drafts)
        )
        self.assertEqual(queryset.count(), total_posts)
        # All posts in the queryset should be present in the database
        all_post_ids = set(Post.objects.values_list("id", flat=True))
        queryset_ids = set(queryset.values_list("id", flat=True))
        self.assertEqual(queryset_ids, all_post_ids)
        

    def test_regular_user_sees_all_posted_posts_and_own_drafts(self):
        request = type("Request", (), {"user": self.user1})()
        queryset = Post.objects.get_authorized_posts(request)

        # expects: 2 posted from user1 + 2 from user2 + 3 from admin = 7
        posted_posts = queryset.filter(posted=True)
        self.assertEqual(posted_posts.count(), 2)
        for post in posted_posts:
            self.assertTrue(post.posted)



    # obvious tests - optional
    def test_post_str_returns_title(self):
        post = PostFactory(title="Hello World")
        self.assertEqual(str(post), "Hello World")


    def test_category_str_returns_name(self):
        self.assertEqual(str(self.cat1), "Nature")
        self.assertEqual(str(self.cat2), "Loisir")
        self.assertEqual(str(self.cat3), "Info")
        self.assertEqual(str(self.cat4), "Event")
