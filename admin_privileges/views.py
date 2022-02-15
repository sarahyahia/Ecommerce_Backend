from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from product.models import Product, Category, ProductChangesLog
from product.serializers import ProductSerializer
from cart.models import Order, OrderItem
from .serializers import CategorySerializer, ProductChangesLogSerializer
from rest_framework.response import Response
from rest_framework import status
from django.forms.models import model_to_dict
import json
from django.utils.timezone import now
import datetime


# to control products 

class AddProductView(APIView): 
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # import pdb; pdb.set_trace()
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
    permission_classes = [IsAdminUser]
    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product_dict = model_to_dict(product)
            product_dict['category_id'] = product_dict.pop('category')
            old_product = Product(**product_dict)
            image = product.image
            thumbnail = product.thumbnail
            Product_fields = [field.name for field in Product._meta.get_fields()]
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                # import pdb; pdb.set_trace()
                serializer.save()
                updated_product = Product.objects.get(pk=pk) 
                differences = list(filter(lambda field: getattr(updated_product, field, None)!= getattr(old_product, field, None), Product_fields))
                differences.remove('date_added')
                if differences:
                    product_dict['image'] = json.dumps(str(product_dict['image']))
                    product_dict['thumbnail'] = json.dumps(str(product_dict['thumbnail']))
                    if 'image' in differences:
                        ProductChangesLog.objects.create(old_product=product_dict, differences= differences, admin= request.user, image=image, thumbnail=thumbnail)
                    else:
                        ProductChangesLog.objects.create(old_product=product_dict, differences= differences, admin= request.user)
                
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
    permission_classes = [IsAdminUser]
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product_dict = model_to_dict(product)
            image = product_dict['image']
            thumbnail = product_dict['thumbnail']
            product_dict['image'] = json.dumps(str(product_dict['image']))
            product_dict['thumbnail'] = json.dumps(str(product_dict['thumbnail']))
            ProductChangesLog.objects.create(old_product=product_dict, admin= request.user, image=image, thumbnail=thumbnail,status='deleted')
            product.delete()
            return Response({'msg': 'The product has been deleted successfully.'},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error': 'The product you want to delete is not found.'},status=status.HTTP_400_BAD_REQUEST)
            

# to control category

class AddCategoryView(APIView):
    permission_classes = [IsAdminUser]
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
    permission_classes = [IsAdminUser]
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
    def post(self, request, category_slug):
        try:
            category = self.get_object(category_slug)
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
    permission_classes = [IsAdminUser]
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
    def get(self, request, category_slug):
        try:
            category = self.get_object(category_slug)
            category.delete()
            return Response({'msg': 'The category has been deleted successfully.'},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error': 'The category you want to delete is not found.'},status=status.HTTP_400_BAD_REQUEST)
            

class SalesByCategory(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        categories = Category.objects.all()
        sales=[]
        for category in categories :
            items = OrderItem.objects.filter(product__category = category)
            sales_for_category = sum(item.quantity * item.product.price for item in items)
            # import pdb; pdb.set_trace()
            # category = CategorySerializer(data=category)
            sales.append({'category' :category.title, 'sales' :sales_for_category})
        return Response(sales,status=status.HTTP_200_OK)


class SalesByVendor(APIView):
    permission_classes = [IsAdminUser]
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
        return Response(sales,status=status.HTTP_200_OK)



class Top10Products(APIView):
    authentication_classes = []
    def get(self, request):
        sales_for_all_products =[]
        for product in Product.objects.all():
            items = OrderItem.objects.filter(product=product)
            sales_for_product = sum(item.product.price for item in items)
            if sales_for_product == 0:
                continue
            sales_for_all_products.append({'product': ProductSerializer(product).data, 'sales':sales_for_product})
        sales_for_all_products = sorted(sales_for_all_products, key=lambda x: x['sales'], reverse=True)
        # import pdb; pdb.set_trace()
        return Response(sales_for_all_products[:10],status=status.HTTP_200_OK)

class Top10ProductsForMonth(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        sales_for_all_products =[]
        for product in Product.objects.all():
            # import pdb; pdb.set_trace()
            items = OrderItem.objects.filter(created_at__month=datetime.date.today().month).filter(product=product)
            sales_for_product = sum(item.product.price for item in items)
            if sales_for_product == 0:
                continue
            sales_for_all_products.append({'product': ProductSerializer(product).data, 'sales':sales_for_product})
        sales_for_all_products = sorted(sales_for_all_products, key=lambda x: x['sales'], reverse=True)
        # import pdb; pdb.set_trace()
        return Response(sales_for_all_products[:10],status=status.HTTP_200_OK)

class Top10Vendors(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        sales =[]
        vendors = []
        for product in Product.objects.all():
            vendors.append(product.vendor)
        vendors = set(vendors)
        for vendor in vendors:
            items = OrderItem.objects.filter(product__vendor= vendor)
            sales_for_vendor = sum(item.quantity * item.product.price for item in items)
            if sales_for_vendor == 0:
                continue
            # import pdb; pdb.set_trace()
            sales.append({'vendor' :vendor, 'sales' :sales_for_vendor})
        sales= sorted(sales,key=lambda x:x['sales'],reverse=True)
        return Response(sales[:10],status=status.HTTP_200_OK)


class Top10VendorsForMonth(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        sales =[]
        vendors = []
        for product in Product.objects.all():
            vendors.append(product.vendor)
        vendors = set(vendors)
        for vendor in vendors:
            items = OrderItem.objects.filter(created_at__month=datetime.date.today().month).filter(product__vendor= vendor)
            sales_for_vendor = sum(item.quantity * item.product.price for item in items)
            if sales_for_vendor == 0:
                continue
            # import pdb; pdb.set_trace()
            sales.append({'vendor' :vendor, 'sales' :sales_for_vendor})
        sales= sorted(sales,key=lambda x:x['sales'],reverse=True)
        return Response(sales[:10],status=status.HTTP_200_OK)
    

class ProductChangesLogList(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        product_changes_log = ProductChangesLog.objects.all()
        serializer = ProductChangesLogSerializer(product_changes_log, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class DeleteProductChangesLogView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, pk):
        try:
            product_changes_log= ProductChangesLog.objects.get(pk=pk)
            # import pdb; pdb.set_trace()
            if product_changes_log.image :
                storage, path = product_changes_log.image.storage, product_changes_log.image.path
                product_changes_log.image.delete()
                storage.delete(path)
            product_changes_log.delete()
            return Response({'msg': 'The log has been deleted successfully.'},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error': 'The log you want to delete is not found.'},status=status.HTTP_400_BAD_REQUEST)
        