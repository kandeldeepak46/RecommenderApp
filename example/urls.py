from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<str:isbn>', views.detail, name='detail'),
    path('getData', views.getData, name='getData'),
]