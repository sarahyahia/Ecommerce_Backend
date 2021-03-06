from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from django.db.models import Q
from django_filters import rest_framework as filters
from .filters import ProductFilter
from rest_framework import generics
from rest_framework.permissions import AllowAny
from profanity_filter import ProfanityFilter


class StandardResultsSetPagination(PageNumberPagination):
    
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class LatestProductsList(APIView):
    authentication_classes = []
    def get(self, request, format=None):
        products = Product.objects.all()[0:6]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):
    authentication_classes = []
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
        
    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class ProductsList(APIView):
    authentication_classes = []
    pagination_class = PageNumberPagination
    def get(self, request, format=None):
        productsList= Product.objects.all().order_by('slug')
        paginator = PageNumberPagination()
        paginator.page_size = 6
        result_page = paginator.paginate_queryset(productsList, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
        


class CategoryDetail(APIView):
    authentication_classes = []
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


class CategoryList(APIView):
    authentication_classes = []
    def get(self, request):
        categories = Category.objects.all()
        serializer= CategorySerializer(categories, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')
    pf = ProfanityFilter()
    query_is_profane=pf.is_profane(query)
    if query_is_profane:
        return Response({'error':pf.censor(query)})
    elif query:
        products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(category__title__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})
    


class ProductFilterList(generics.ListAPIView):
    authentication_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter
    def test_func(self,request):
        pf = ProfanityFilter()
        title_is_profane=pf.is_profane(request.data.get('title'))
        vendor_is_profane = pf.is_profane(request.data.get('vendor'))
        if title_is_profane or vendor_is_profane:
            return False
        return True
    