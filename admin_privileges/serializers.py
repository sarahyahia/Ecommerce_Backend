from rest_framework import serializers

from product.models import Category, ProductChangesLog

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            "id",
            "title",
            'slug',
            'description',
        )

class ProductChangesLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductChangesLog
        fields = (
            'old_product',
            'differences',
            'admin',
            'date_added',
            'status',
            'image',
        )