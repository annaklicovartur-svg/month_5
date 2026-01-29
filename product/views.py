from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from .serializers import ProductListSer

@api_view(['GET'])
def products_list_api_view(request):
    products = Product.objects.all()
    data = ProductListSer(products, many=True).data
    return Response(
        data={"text": "Hello, World!"},
    )