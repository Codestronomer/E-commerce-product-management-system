from django.test import TestCase
from product_management.models import Product, Category, Discount, DiscountType
from product_management.serializers import ProductSerializer, DiscountSerializer, CategorySerializer

class ProductSerializerTest(TestCase):
  def setUp(self):
    """Setup Mock Objects"""
    self.category = Category.objects.create(title="Macbooks", description="All models of Macbooks")
    self.product = Product.objects.create(
      name="Macbook Pro M4",
      description="Apple macbook pro m4 series, 16inches, 20gb ram, 512 ssd storage",
      price=2500.99,
      quantity=10,
      status="active",
      category=self.category
    )
    self.product_data = {
      "name": "Macbook Pro M4",
      "description": "Apple macbook pro m4 series, 16inches, 20gb ram, 512 ssd storage",
      "price": 2500.99,
      "quantity": 10,
      "status": "active",
      "category": self.category.id
    }
    
  def test_serializer_with_valid_input_data(self):
    """Test for valid input data"""
    serializer = ProductSerializer(data=self.product_data)
    self.assertTrue(serializer.is_valid())
    self.assertEqual(serializer.validated_data["name"], "Macbook Pro M4")
    self.assertEqual(serializer.validated_data["category"], self.category)
    
  def test_serializer_with_invalid_price(self):
    """Test for invalid price data"""
    self.product_data["price"] = -10  # Negative price

    serializer = ProductSerializer(data=self.product_data)
    self.assertFalse(serializer.is_valid())
    self.assertIn("price", serializer.errors)
    self.assertIn("Ensure this value is greater than or equal to 0.", serializer.errors["price"][0])
  
  def test_discounted_price_without_active_discount(self):
    """Test if discounted price returns the original price when no active discount is available"""
    serializer = ProductSerializer(instance=self.product)
    self.assertEqual(serializer.data['discounted_price'], self.product.price)

  def test_discounted_price_with_active_percentage_discount(self):
    """Test if discounted price is calculated correctly when there's an active percentage discount"""
    discount = Discount.objects.create(
      product=self.product,
      value=20,
      discount_type=DiscountType.PERCENTAGE,
      status='active'
    )
    serializer = ProductSerializer(instance=self.product)
    expected_discounted_price = self.product.price * (1 - discount.value / 100)
    self.assertEqual(serializer.data['discounted_price'], expected_discounted_price)

  def test_discounted_price_with_active_fixed_discount(self):
    """Test if discounted price is calculated correctly when there's an active fixed discount"""
    discount = Discount.objects.create(
      product=self.product,
      value=200,
      discount_type=DiscountType.FIXED,
      status='active'
    )
    serializer = ProductSerializer(instance=self.product)
    expected_discounted_price = self.product.price - discount.value
    self.assertEqual(serializer.data['discounted_price'], expected_discounted_price)
  
  def test_serializer_with_missing_fields(self):
    """Test for missing required fields in the serializer"""
    incomplete_data = {
      "name": "Macbook Pro M4",
    }

    serializer = ProductSerializer(data=incomplete_data)
    self.assertFalse(serializer.is_valid())
    self.assertIn("price", serializer.errors)
    self.assertIn("category", serializer.errors)