from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from product.models import Product, Category
from product.serializers import ProductSerializer
from cart.models import Order, OrderItem
from .serializers import CategorySerializer
from rest_framework.response import Response
from rest_framework import status




# to control products 

class AddProductView(APIView): 
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success":True,
                "msg":"The product has been created successfuly",
                'data':serializer.data
            },status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            'msg': 'There is an error, please try again.',
            "errors": serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)

class EditProductView(APIView): 
    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success":True,
                    "msg":"The product has been modified successfuly",
                    'data':serializer.data
                },status=status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors})
        except Exception as e:
            return Response({
                "success": False,
                'error': 'The product you want to edit is not found.',
                "errors": str(e)
            },status=status.HTTP_400_BAD_REQUEST)
        
        
        
class DeleteProductView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response({'msg': 'The product has been deleted successfully.'},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error': 'The product you want to delete is not found.'},status=status.HTTP_400_BAD_REQUEST)
            

# to control category

class AddCategoryView(APIView):
    def post(self, request,):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success":True,
                "msg":"The category has been created successfuly",
                'data':serializer.data
            },status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            'msg': 'There is an error, please try again.',
            "errors": serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    
    
    
class EditCategoryView(APIView): 
    def post(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success":True,
                    "msg":"The category has been modified successfuly",
                    'data':serializer.data
                },status=status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors})
        except Exception as e:
            return Response({
                "success": False,
                'error': 'The category you want to edit is not found.',
                "errors": str(e)
            },status=status.HTTP_400_BAD_REQUEST)
        
        
        
class DeleteCategoryView(APIView):
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response({'msg': 'The category has been deleted successfully.'},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error': 'The category you want to delete is not found.'},status=status.HTTP_400_BAD_REQUEST)
            

class SalesByCategory(APIView):
    def get(self, request):
        categories = Category.objects.all()
        sales=[]
        for category in categories :
            items = OrderItem.objects.filter(product__category = category)
            sales_for_category = sum(item.quantity * item.product.price for item in items)
            # import pdb; pdb.set_trace()
            # category = CategorySerializer(data=category)
            sales.append({'category' :category.title, 'sales' :sales_for_category})
        return Response({'sales':sales},status=status.HTTP_200_OK)


class SalesByVendor(APIView):
    def get(self, request):
        sales =[]
        vendors = []
        for product in Product.objects.all():
            vendors.append(product.vendor)
        vendors = set(vendors)
        for vendor in vendors:
            items = OrderItem.objects.filter(product__vendor= vendor)
            sales_for_vendor = sum(item.quantity * item.product.price for item in items)
            # import pdb; pdb.set_trace()
            sales.append({'vendor' :vendor, 'sales' :sales_for_vendor})
        return Response({'sales':sales},status=status.HTTP_200_OK)
        