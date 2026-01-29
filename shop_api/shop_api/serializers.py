from rest_framework import serializers
from .models import Product

class ProductListSer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'titile test from serializers.py'.split()