from rest_framework import serializers

from .models import Category, Product

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "get_absolute_url",
            "description",
            "price",
            'status',
            "get_image",
            "get_thumbnail",
            'vendor',
            'quantity_available'
        )

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "title",
            "get_absolute_url",
            "products",
        )