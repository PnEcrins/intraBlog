from django.test import TestCase, RequestFactory
from django.contrib.auth.models import Group
from django.contrib.admin.sites import AdminSite
from blog.models import Post, Category
from blog.admin import PostAdmin, CategoryAdmin, PUBLISHER_GROUP_NAME
from blog.tests.factories import UserFactory, SuperUserFactory, PostFactory, CategoryFactory


class AdminTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.site = AdminSite()

        self.admin_user = SuperUserFactory()
        self.user = UserFactory()
        self.publisher = UserFactory()
        self.publisher_group = Group.objects.create(name=PUBLISHER_GROUP_NAME)
        self.publisher.groups.add(self.publisher_group)
        self.publisher.save()

        self.post_by_publisher = PostFactory(author=self.publisher, posted=False)
        self.post_by_user = PostFactory(author=self.user, posted=True)

        self.category = CategoryFactory()

        self.post_admin = PostAdmin(Post, self.site)
        self.category_admin = CategoryAdmin(Category, self.site)

    # Test that superuser sees 'author' field in PostAdmin
    def test_get_fields_superuser(self):
        request = self.factory.get("/")
        request.user = self.admin_user
        fields = self.post_admin.get_fields(request)
        self.assertIn("author", fields)

    # Test that non-superuser does not see 'author' field in PostAdmin
    def test_get_fields_non_superuser(self):
        request = self.factory.get("/")
        request.user = self.publisher
        fields = self.post_admin.get_fields(request)
        self.assertNotIn("author", fields)

    # Test that superuser sees all posts in PostAdmin queryset
    def test_get_queryset_superuser(self):
        request = self.factory.get("/")
        request.user = self.admin_user
        qs = self.post_admin.get_queryset(request)
        self.assertIn(self.post_by_user, qs)
        self.assertIn(self.post_by_publisher, qs)

    # Test that publisher sees all posts in PostAdmin queryset
    def test_get_queryset_publisher(self):
        request = self.factory.get("/")
        request.user = self.publisher
        qs = self.post_admin.get_queryset(request)
        self.assertIn(self.post_by_publisher, qs)
        self.assertIn(self.post_by_user, qs)

    # Test that superuser can change any post
    def test_has_change_permission_superuser(self):
        request = self.factory.get("/")
        request.user = self.admin_user
        self.assertTrue(self.post_admin.has_change_permission(request, self.post_by_user))

    # Test that post owner can change their own post
    def test_has_change_permission_owner(self):
        request = self.factory.get("/")
        request.user = self.publisher
        self.assertTrue(self.post_admin.has_change_permission(request, self.post_by_publisher))

    # Test that publisher cannot change someone else's post
    def test_has_change_permission_other(self):
        request = self.factory.get("/")
        request.user = self.publisher
        self.assertFalse(self.post_admin.has_change_permission(request, self.post_by_user))

    # Test that superuser can delete any post
    def test_has_delete_permission_superuser(self):
        request = self.factory.get("/")
        request.user = self.admin_user
        self.assertTrue(self.post_admin.has_delete_permission(request, self.post_by_user))

    # Test that post owner can delete their own post
    def test_has_delete_permission_owner(self):
        request = self.factory.get("/")
        request.user = self.publisher
        self.assertTrue(self.post_admin.has_delete_permission(request, self.post_by_publisher))

    # Test that publisher cannot delete someone else's post
    def test_has_delete_permission_other(self):
        request = self.factory.get("/")
        request.user = self.publisher
        self.assertFalse(self.post_admin.has_delete_permission(request, self.post_by_user))

    # Test that save_model sets author to current user if not set
    def test_save_model_sets_author(self):
        request = self.factory.post("/")
        request.user = self.publisher
        post = PostFactory.build(author=None)
        form = None
        self.post_admin.save_model(request, post, form, change=False)
        self.assertEqual(post.author, self.publisher)

    # Test that superuser has all permissions on CategoryAdmin
    def test_category_admin_permissions_superuser(self):
        request = self.factory.get("/")
        request.user = self.admin_user
        self.assertTrue(self.category_admin.has_module_permission(request))
        self.assertTrue(self.category_admin.has_view_permission(request))
        self.assertTrue(self.category_admin.has_add_permission(request))
        self.assertTrue(self.category_admin.has_change_permission(request))
        self.assertTrue(self.category_admin.has_delete_permission(request))

    # Test that normal user has no permissions on CategoryAdmin
    def test_category_admin_permissions_normal_user(self):
        request = self.factory.get("/")
        request.user = self.user
        self.assertFalse(self.category_admin.has_module_permission(request))
        self.assertFalse(self.category_admin.has_view_permission(request))
        self.assertFalse(self.category_admin.has_add_permission(request))
        self.assertFalse(self.category_admin.has_change_permission(request))
        self.assertFalse(self.category_admin.has_delete_permission(request))
