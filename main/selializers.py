from rest_framework import serializers
from product.models import Product

class ProductDetailSer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductListSer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'titile test from serializers.py'.split()