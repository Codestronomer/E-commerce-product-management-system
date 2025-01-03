from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import Category, Product, Discount
from .serializers import CategorySerializer, ProductSerializer, DiscountSerializer
from typing import List
from drf_yasg.utils import swagger_auto_schema

class CategoryViewSet(viewsets.ModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  pagination_class = None
  

class ProductView(GenericAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer

  def post(self, request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def get(self, request):
    products: List[Product] = Product.objects.all()

    # Filter by category
    category_id = request.query_params.get('category')
    if category_id:
      products = products.filter(category__id=category_id)

    paginator = self.paginate_queryset(products)
    if paginator is not None:
      serializer = ProductSerializer(paginator, many=True)
      return self.get_paginated_response(serializer.data)
    
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
  
class ProductDetailView(APIView):
  def get(self, request, pk, *args, **kwargs):
    try:
      product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
      return Response({ 'error': f'Product with id - {pk} not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductSerializer(product)
    return Response(serializer.data)
  

class DiscountView(APIView):
  @swagger_auto_schema(
        operation_description="Create a new discount",
        request_body=DiscountSerializer,
        responses={
            201: DiscountSerializer,
            400: 'Bad Request - Invalid data provided'
        }
    )
  def post(self, request):
    serializer = DiscountSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class ApplyDiscountToProductView(APIView):
  """ Apply an existing discount to a product """
  def post(self, request, product_id, discount_id):
    try:
      product = Product.objects.get(id=product_id)

      discount = Discount.objects.get(id=discount_id)

      product.discounts.add(discount)

      # Apply the discount
      discounted_price = discount.apply_discount(product.price)

      # return details along with discounted price
      serializer = ProductSerializer(product)
      return Response({
          "product": serializer.data,
          "discounted_price": round(discounted_price, 2)
      }, status=status.HTTP_200_OK)

    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    except Discount.DoesNotExist:
        return Response({"error": "Discount not found."}, status=status.HTTP_404_NOT_FOUND)