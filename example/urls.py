from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<str:isbn>', views.detail, name='detail'),
    path('getData', views.getData, name='getData'),
    path('search', views.search, name='search'),
    path('barcode', views.barcode, name='barcode'),
    path('add_book', views.add_book, name='add_book')
]