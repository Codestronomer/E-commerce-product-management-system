from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import Category, Product, Discount
from .serializers import CategorySerializer, ProductSerializer, DiscountSerializer
from typing import List

class CategoryViewSet(viewsets.ModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  pagination_class = None

  def list(self, request, *args, **kwargs):
    queryset = self.get_queryset()
    return Response(self.get_serializer(queryset, many=True).data)
  

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
  def post(self, request, *args, **kwargs):
    serializer = DiscountSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)