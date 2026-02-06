from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from product.models import Product, Review, Category
from .selializers import ProductListSer, ProductDetailSer, CategoryListSer, CategoryDetailSer, ReviewListSer, ReviewDetailtSer, ProductWithReviewsSerializer, ReviewForProductSerializer


# GET all
@api_view(['GET', 'POST'])
def products_list_api_view(request):
    if request.method == 'GET':
        # Step 1: Collect all objects from DB (QuerySet)
        products = Product.objects.all()

        # Step 2: Reformat (Serialize) queryset to list of dictionary
        data = ProductListSer(products, many=True).data

        # Step 3: Return response
        return Response(
            data=data,
        )
    elif request.method == 'POST':
        # step 1: Получение данных от клиента from RequestBody
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category_id')

        print(title, description, price, category_id)
        # step 2: Create product by recived data
        product = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category_id=category_id
        )
        # step 3: Return Response
        return Response(status=status.HTTP_201_CREATED,
                   data=ProductDetailSer(product).data)



# get only 1 object
@api_view(['GET', 'PUT', 'DELETE'])
def products_detail_api_view(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'GET':
        data = ProductDetailSer(product, many=False).data
        return Response(
            data=data
    )
    elif request.method == 'PUT':
        product.title == request.method.data.get('title') # request.method - Это действия ввода или вывода от клиента ..... request.method.data.get - действия клиента превращаются в базу данных для запроса (нам выдается действия клиента request.method мы превращаем их в бд .data и получаем .get)
        product.description == request.method.data.get('description')
        product.price == request.method.data.get('price')
        product.category_id == request.method.data.get('category_id')
        # WE use .set with manyTOmany and use .save(), after the .set method

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  # Delete is forever




@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        data = CategoryListSer(categories, many=True).data
        return Response (
            data=data
        )
    elif request.method == 'POST':
        name = request.data.get('name')
        print(name)

        category = Category.objects.create(
            name=name
        )
        return Response(status=status.HTTP_201_CREATED,
                   data=CategoryDetailSer(category).data)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    if request.method == 'GET':
        categories = Category.objects.get(id=id)
        data = CategoryDetailSer(categories, many=False).data
        return Response (
            data=data
        )
    
    elif request.method == 'PUT':
        categories.name = request.data.get('name')

    elif request.method == 'DELETE':
        categories.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewListSer(reviews, many=True).data
        return Response(
            data=data
        )
    elif request.method == 'POST':
        text = request.data.get('text')
        stars = request.data.get('stars')
        product_id = request.data.get('product_id')
        print(text, stars, product_id)

        reviews = Review.objects.create(
            text = text,
            stars = stars,
            product_id = product_id,
        )
        return Response(status=status.HTTP_201_CREATED,
                   data=ReviewDetailtSer(reviews).data)



@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    reviews = Review.objects.get(id=id)
    if request.method == 'GET':
        data = ReviewDetailtSer(reviews, many=False).data
        return Response(
            data=data
        )
    elif request.method == 'PUT':
        reviews.text = request.data.get('text')
        reviews.stars = request.data.get('stars')
        reviews.product_id = request.data.get('product_id')
        

    elif request.method == 'DELETE':
        reviews.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
def products_with_reviews_api_view(request):

    # Используем prefetch_related для оптимизации запросов
    products = Product.objects.prefetch_related('reviews').all()
    
    # Сериализуем данные
    serializer = ProductWithReviewsSerializer(products, many=True)
    
    return Response(serializer.data)





