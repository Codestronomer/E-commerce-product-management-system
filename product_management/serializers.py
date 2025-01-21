from rest_framework import serializers
from decimal import Decimal
from .models import Category, Product, Discount, DiscountStatus, DiscountType

class CategorySerializer(serializers.ModelSerializer):
  subcategories = serializers.SerializerMethodField()
  class Meta:
    model = Category
    fields = ['id', 'title', 'description', 'parent', 'slug', 'created_at', 'updated_at', 'subcategories']

  def validate(self, category):
    """Ensure category isn't trying to set itself as it's parent"""
    parent = category.get("parent")

    if parent and self.instance and parent.id == self.instance.id:
      raise serializers.ValidationError("A category cannot be it's own parent.")
    return category
  
  def get_subcategories(self, obj):
    """Return the subcategories of the current category"""
    subcategories = Category.objects.filter(parent=obj)
    return CategorySerializer(subcategories, many=True).data

class ProductSerializer(serializers.ModelSerializer):
  category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
  discounted_price = serializers.SerializerMethodField()

  class Meta:
    model = Product
    fields = ['id', 'name', 'description', 'price', 'quantity', 'status', 'category', 'created_at', 'updated_at', 'discounted_price']

  def validate_price(self, value):
    """Prevent negative price value"""
    if value < 0:
        raise serializers.ValidationError("Price cannot be negative.")
    return value

  def get_discounted_price(self, obj: Product):
    """Get the discounted price for a product"""
    active_discounts = obj.discounts.filter(status='active')
    
    if active_discounts.exists():
      # Get the best discount and apply it to the price
      best_discount = max(active_discounts, key=lambda x: self.apply_highest_discount(x, obj.price))
      # Apply discount and return rounded discounted price
      return best_discount.apply_discount(obj.price)
    
    # If no active discount, return the original price rounded to 2 decimal places
    return round(obj.price, 2)

  def apply_highest_discount(self, discount: Discount, price: Decimal):
    """Retrieve the highest discount value for the product price"""
    if discount.discount_type == DiscountType.PERCENTAGE:
      # Apply percentage discount
      return float(price) * float(discount.value) / 100
    elif discount.discount_type == DiscountType.FIXED:
      # Apply fixed discount
      return discount.value
    return Decimal(0)
  
class DiscountSerializer(serializers.ModelSerializer):
  class Meta:
    model = Discount
    fields = ['id', 'product', 'discount_type', 'value', 'status', 'expires_at']

  def create(self, validated_data):
    return Discount.objects.create(**validated_data)

  # example schema fields for swagger schema
  product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
  discount_type = serializers.ChoiceField(choices=DiscountType.choices)
  value = serializers.DecimalField(max_digits=10, decimal_places=2)
  status = serializers.ChoiceField(choices=DiscountStatus.choices)
  expires_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
