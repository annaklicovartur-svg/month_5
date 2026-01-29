from django.contrib import admin
from django.urls import path
from main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/categories/', views.products_list_api_view),
    path('/api/v1/categories/<int:id>/', views.products_detail_api_view)
]
