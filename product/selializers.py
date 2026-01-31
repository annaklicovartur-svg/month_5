from rest_framework import serializers
from product.models import Product, Category, Review

class ReviewForProductSerializer(serializers.ModelSerializer):
    stars_display = serializers.CharField(source='get_stars_display', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'stars_display']


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewForProductSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'average_rating']
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            total_stars = sum(review.stars for review in reviews)
            return round(total_stars / reviews.count(), 2)
        return 0

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
        fields = ['id','text', 'product', 'stars']

class ReviewDetailtSer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

       