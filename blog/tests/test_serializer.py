from django.test import TestCase
from blog.serializers import PostSerializer
from blog.tests.factories import PostFactory, CategoryFactory


class PostSerializerTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = CategoryFactory(name="Nature")
        cls.post = PostFactory(categories=[cls.category])


    def test_post_serializer_fields_and_types(self):
        serializer = PostSerializer(instance=self.post)
        data = serializer.data

        # expected fields
        expected_fields = {
            'id',
            'title',
            'content',
            'created_at',
            'updated_at',
            'posted',
            'image',
            'author_first_name',
            'author_last_name',
            'categories',
            'category_names'
        }
        assert expected_fields.issubset(set(data.keys()))

        # Datatype checks
        self.assertIsInstance(data['id'], int)
        self.assertIsInstance(data['title'], str)
        self.assertIsInstance(data['content'], str)
        self.assertIsInstance(data['created_at'], str)
        self.assertIsInstance(data['updated_at'], str)
        self.assertIsInstance(data['posted'], bool)
        self.assertIn('image', data)  # can be None
        self.assertTrue(isinstance(data['author'], int) or data['author'] is None)
        self.assertIsInstance(data['author_first_name'], str)
        self.assertIsInstance(data['author_last_name'], str)

        self.assertIsInstance(data['categories'], list)
        self.assertGreaterEqual(len(data['categories']), 1)
        self.assertIsInstance(data['categories'][0], int)

        self.assertIsInstance(data['category_names'], list)
        self.assertGreaterEqual(len(data['category_names']), 1)
        self.assertIsInstance(data['category_names'][0], str)
