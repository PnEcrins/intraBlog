from django.test import TestCase
from rest_framework.test import APIClient
from blog.tests.factories import CategoryFactory

class CategoryAPITestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()

        # Create categories
        cls.cat1 = CategoryFactory(name="Nature")
        cls.cat2 = CategoryFactory(name="Loisir")
        cls.cat3 = CategoryFactory(name="Info")
        cls.cat4 = CategoryFactory(name="Event")

    def test_get_all_categories(self):
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)  # 4 categories created

    def test_get_single_category(self):
        response = self.client.get(f"/api/categories/{self.cat1.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Nature")