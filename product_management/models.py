from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from time import timezone

class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subcategories')
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
  
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(validators=[MinValueValidator(0)], default=1)
    status = models.CharField(max_length=20, choices=ProductStatus.choices, default=ProductStatus.ACTIVE, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Define Discount type Enum
class DiscountType(models.TextChoices):
    PERCENTAGE = 'percentage', 'Percentage'
    FIXED = 'fixed', 'Fixed Amount'

class DiscountStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'


class Discount(models.Model):
    product = models.ForeignKey(Product, related_name='discounts', on_delete=models.CASCADE, db_index=True)
    discount_type = models.CharField(max_length=10, choices=DiscountType.choices, db_index=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=DiscountStatus.choices, default=DiscountStatus.ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.get_discount_type_display()} - {self.value}'
    
    def apply_discount(self, price):
        """Apply the discount to a given price of a product"""
        discount_functions = {
            DiscountType.FIXED: lambda price: price - self.value,
            DiscountType.PERCENTAGE: lambda price: price - (price * self.value / 100) 
        }

        return discount_functions.get(self.discount_type, lambda price: price)(price)
    
    def is_valid(self):
        """ Check if discount hasn't expired or is inactive"""
        if self.expires_at:
          return self.expires_at >= timezone.now() and self.status == DiscountStatus.ACTIVE
        return True
        