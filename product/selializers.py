from rest_framework import serializers
from product.models import Product, Category, Review

# GET only one object
class ProductDetailSer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# GET all objects
class ProductListSer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category']

class CategoryListSer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryDetailSer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ReviewListSer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','text', 'product']

class ReviewDetailtSer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        