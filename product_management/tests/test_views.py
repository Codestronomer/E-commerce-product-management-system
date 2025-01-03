from rest_framework.test import APITestCase
from rest_framework import status
from product_management.models import Category, Product

class CategoryViewSetTest(APITestCase):
  def setUp(self):
    self.category = Category.objects.create(title="Electronics", description="All electronic products")

  def test_list_categories(self):
    response = self.client.get("/api/categories/")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)

  def test_create_category(self):
    data = {
      "title": "Furniture",
      "description": "All kinds of furniture products"
    }

    response = self.client.post("/api/categories/", data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['title'], "Furniture")

  def test_sub_categories(self):
    subcategory = Category.objects.create(
      title="Laptops",
      description="All Laptops and laptop accessories",
      parent=self.category
    )
    response = self.client.get("/api/categories/")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn("subcategories", response.data[0])

  def test_category_is_unique(self):
        # Attempt to create a second category with the same title
        data = {
            "title": "Electronics",  # Same title as the first one
            "description": "Duplicate category"
        }

        response = self.client.post("/api/categories/", data)

        # Assert that the status code is 400 for a bad request (due to validation error)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that the error message contains something about the title being non-unique
        self.assertIn('title', response.data)
        self.assertIn('category with this title already exists.', response.data['title'][0])

  
class ProductViewSetTest(APITestCase):
  def setUp(self):
    self.category = Category.objects.create(title="Electronics", description="All electronic products")
    self.products = [Product.objects.create(
      name=f'Product - {i}',
      price=10,
      quantity=5,
      category=self.category,
    ) for i in range(15)]
    
  def test_paginated_products(self):
    response = self.client.get("/api/products/?page_size=10")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTrue("next" in response.data)
    self.assertEqual(len(response.data["results"]), 10)