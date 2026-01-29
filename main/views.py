from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from .selializers import ProductListSer, ProductDetailSer

@api_view(['GET'])
def products_detail_api_view(request, id):
    product = Product.objects.get(id=id)
    data = ProductDetailSer(products, many=False).data
    return Response(data=data)

@api_view(['GET'])
def products_list_api_view(request):
    products = Product.objects.all()
    data = ProductListSer(products, many=True).data
    return Response(
        data={"text": "Hello, World!"},
    )