from django.urls import path
from .views import LatestProductsList, ProductDetail, CategoryDetail, ProductsList, CategoryList, search, ProductFilterList



urlpatterns = [
    path('products/search/query/', search),
    path('products/search/', ProductFilterList.as_view()),
    path('latestproduct/', LatestProductsList.as_view()),
    path('products/<slug:category_slug>/<slug:product_slug>/', ProductDetail.as_view()),
    path('products/', ProductsList.as_view()),
    path('categories/', CategoryList.as_view()),
    path('category/<slug:category_slug>/', CategoryDetail.as_view()),
]