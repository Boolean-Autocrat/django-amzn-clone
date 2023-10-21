import json
import requests
from django.test import TestCase
from .models import Product, Category
from datetime import datetime


class FakeStoreAPITestCase(TestCase):
    FAKE_STORE_API_URL = "https://fakestoreapi.com/products"

    def fetch_products_from_fake_api(self):
        response = requests.get(self.FAKE_STORE_API_URL)
        if response.status_code == 200:
            return response.json()
        return []

    def test_fetch_and_save_products(self):
        # Make 10 requests to the fake store API
        for _ in range(10):
            products = self.fetch_products_from_fake_api()

            # Iterate over the products and save them to the database
            for product_data in products:
                category = Category(
                    name=product_data["category"],
                    slug=product_data["category"].replace(" ", "-"),
                )
                category.save()

                product = Product(
                    name=product_data["title"],
                    img=product_data["image"],
                    price=product_data["price"],
                    stock=10,
                    description=product_data["description"],
                    slug=product_data["title"].replace(" ", "-"),
                    # random date and time
                    manufactured_on=datetime.now(),
                    features=product_data["description"],
                )
                product.save()

        # Check if 10 products were saved
        self.assertEqual(Product.objects.count(), 10)
