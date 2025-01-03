from django.test import TestCase
from django.core.exceptions import ValidationError
from product_management.models import Category, Discount, Product

class CategoryModelTest(TestCase):
  def setUp(self):
    """Set up test for category"""
    self.category = Category.objects.create(title="Electronics", description="All electronic products")

  def test_creation(self):
    """Test category creation"""
    self.assertEqual(self.category.title, "Electronics")

  def test_slug_generation(self):
    """Test that slug is properly generated from category title"""
    self.assertIsNotNone(self.category.slug)


class ProductModelTest(TestCase):
  def setUp(self):
    """Set up test for product"""
    self.category = Category.objects.create(title="Electronics", description="All electronic products")
    self.product = Product.objects.create(
      name="Macbook Pro M3",
      description="Apple macbook pro m3 series, 14inches, 16gb ram, 512 ssd storage",
      price=2100.99,
      quantity=20,
      category=self.category
    )

  def test_creation(self):
    """ Test product creation"""
    self.assertEqual(self.product.name, "Macbook Pro M3")
    self.assertEqual(self.product.description, "Apple macbook pro m3 series, 14inches, 16gb ram, 512 ssd storage")
  
  def test_quantity_validation(self):
    """Test that quantity validation works (quantity is not non-negative)"""
    self.assertGreater(self.product.quantity, 0)

  def test_price_validation(self):
    """Test that price is non-negative"""
    self.product = Product.objects.create(
      name="Macbook Pro M3",
      description="Apple macbook pro m3 series, 14inches, 16gb ram, 512 ssd storage",
      price=2100.99,
      quantity=-20,
      category=self.category
    )
    with self.assertRaises(ValidationError):
      self.product.full_clean()