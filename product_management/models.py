from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from time import timezone
from decimal import Decimal

class Category(models.Model):
  """Represents a category in the ecommerce system"""

  title = models.CharField(max_length=255, unique=True)
  description = models.TextField(blank=True)
  parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subcategories')
  slug = models.SlugField(max_length=100, unique=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


  def __str__(self):
    return self.title

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title)[:100]
    super().save(*args, **kwargs)


# Define Status enum
class ProductStatus(models.TextChoices):
  ACTIVE = 'active', 'Active'
  INACTIVE = 'inactive', 'Inactive'
  OUT_OF_STOCK = 'out-of-stock', 'Out of Stock'

class Product(models.Model):
  """Represents a product in the ecommerce system"""

  name = models.CharField(max_length=255)
  description = models.TextField(blank=True)
  price = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    validators=[MinValueValidator(0, message="Price cannot be non-negative")]
  )
  quantity = models.IntegerField(validators=[MinValueValidator(0)], default=1)
  status = models.CharField(max_length=20, choices=ProductStatus.choices, default=ProductStatus.ACTIVE, db_index=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE, db_index=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name


# Define Discount type Enum
class DiscountType(models.TextChoices):
  PERCENTAGE = 'percentage', 'Percentage'
  FIXED = 'fixed', 'Fixed Amount'

class DiscountStatus(models.TextChoices):
  ACTIVE = 'active', 'Active'
  INACTIVE = 'inactive', 'Inactive'


class Discount(models.Model):
  """ Represent a discount object in the ecommerce system """

  product = models.ForeignKey(Product, related_name='discounts', on_delete=models.CASCADE, db_index=True)
  discount_type = models.CharField(max_length=10, choices=DiscountType.choices, db_index=True)
  value = models.DecimalField(max_digits=10, decimal_places=2)
  status = models.CharField(max_length=10, choices=DiscountStatus.choices, default=DiscountStatus.ACTIVE, db_index=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  expires_at = models.DateTimeField(null=True, blank=True)

  def __str__(self):
    return f'{self.get_discount_type_display()} - {self.value}'
  
  def apply_discount(self, price: Decimal) -> Decimal:
    """Apply the discount to a given price of a product"""

    if price < 0:
      raise ValueError('Price cannot be less than zero.')

    # Convert the discount value to a Decimal for proper calculation
    discount_value = Decimal(self.value) / Decimal(100)

    if self.discount_type == DiscountType.FIXED:
      discounted_price = price - Decimal(self.value)
    elif self.discount_type == DiscountType.PERCENTAGE:
      discounted_price = price - (price * discount_value)
    else:
      discounted_price = price

    return discounted_price
    
  def is_valid(self):
    """ Check if discount hasn't expired or is inactive"""
    if self.status != DiscountStatus.ACTIVE:
      return False
    if self.expires_at and self.expires_at >= timezone.now():
      return False
    return True
        