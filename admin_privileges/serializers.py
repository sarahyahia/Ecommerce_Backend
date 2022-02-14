from rest_framework import serializers

from product.models import Category, ProductChangesLog
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', )


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
    admin = UserSerializer()
    class Meta:
        model = ProductChangesLog
        fields = (
            'id',
            'old_product',
            'differences',
            'admin',
            'date_added',
            'status',
            'image',
        )