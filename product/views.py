from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from product.models import Product, Review, Category
from .selializers import ProductListSer, ProductDetailSer, CategoryListSer, CategoryDetailSer, ReviewListSer, ReviewDetailtSer


# GET all
@api_view(['GET'])
def products_list_api_view(request):
    # Step 1: Collect all objects from DB (QuerySet)
    products = Product.objects.all()

    # Step 2: Reformat (Serialize) queryset to list of dictionary
    data = ProductListSer(products, many=True).data

    # Step 3: Return response
    return Response(
        data=data,
    )

# get only 1 object
@api_view(['GET'])
def products_detail_api_view(request, id):
    product = Product.objects.get(id=id)
    data = ProductDetailSer(product, many=False).data
    return Response(
        data=data
    )

@api_view(['GET'])
def category_list_api_view(request):
    categories = Category.objects.all()
    data = CategoryListSer(categories, many=True).data
    return Response (
        data=data
    )

@api_view(['GET'])
def category_detail_api_view(request, id):
    categories = Category.objects.get(id=id)
    data = CategoryDetailSer(categories, many=False).data
    return Response (
        data=data
    )

@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    data = ReviewListSer(reviews, many=True).data
    return Response(
        data=data
    )

@api_view(['GET'])
def review_detail_api_view(request, id):
    reviews = Review.objects.get(id=id)
    data = ReviewDetailtSer(reviews, many=False).data
    return Response(
        data = data 
    )
