from rest_framework import serializers
from .models import Category, Product, Discount, DiscountStatus, DiscountType

class CategorySerializer(serializers.Serializer):
  class Meta:
    model = Category
    fields = ['id', 'title', 'description', 'parent', 'slug', 'created_at', 'updated_at']

class ProductSerializer(serializers.Serializer):
  category = CategorySerializer()
  discounted_price = serializers.SerializerMethodField()

  class Meta:
    model = Product
    fields = ['id', 'name', 'description', 'price', 'quantity', 'status', 'category', 'created_at', 'updated_at', 'discounted_price']

  def get_discounted_price(self, obj: Product):
    active_discounts = obj.discounts.filter(status='active')
    if active_discounts.exists():
      # Get the best discount and applies it on the price
      best_discount: Discount = max(active_discounts, key=lambda x: self.apply_best_discount(x, obj.price))

      return best_discount.apply_discount(obj.price)
    
    return obj.price
  
  def apply_best_discount(self, discount: Discount, price: float):
    if discount.discount_type == DiscountType.PERCENTAGE:
      return price * discount.value / 100
    elif discount.discount_type == DiscountType.FIXED:
      return discount.value
    return 0
  
class DiscountSerializer(serializers.Serializer):
  class Meta:
    model = Discount
    fields = ['id', 'product', 'discount_type', 'value', 'status', 'expires_at', 'created_at', 'updated_at']

      
