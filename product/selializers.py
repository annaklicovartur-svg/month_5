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

    def validate_name(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Название товара должно содержать не менее 5 символов.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше нуля.")
        return value

    def validate_article(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("Артикул может содержать только буквы и цифры.")
        if Product.objects.filter(article=value).exists():
            raise serializers.ValidationError("Товар с таким артикулом уже существует.")
        return value

class CategoryListSer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Название категории должно содержать не менее 3 символов.")

        if Category.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Категория с таким названием уже существует.")
        return value

class CategoryDetailSer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ReviewListSer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','text', 'product', 'stars']
        
    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5.")
        return value

    def validate_text(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Текст отзыва должен содержать не менее 10 символов.")
        return value

    def validate(self, data):
        return data

class ReviewDetailtSer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

       