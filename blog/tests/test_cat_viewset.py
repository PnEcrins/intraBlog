from django.test import TestCase
from rest_framework.test import APIClient
from blog.tests.factories import CategoryFactory

class CategoryAPITestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()

        # Create categories and store them in a list
        cls.categories = [
            CategoryFactory(name="Nature"),
            CategoryFactory(name="Loisir"),
            CategoryFactory(name="Info"),
            CategoryFactory(name="Event"),
        ]

    def test_get_all_categories(self):
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), len(self.categories))
        
    def test_get_single_category(self):
        response = self.client.get(f"/api/categories/{self.categories[0].id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Nature")