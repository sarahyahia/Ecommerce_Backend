from django.urls import path
from .views import AddProductView, EditProductView, DeleteProductView, AddCategoryView, EditCategoryView, DeleteCategoryView,SalesByCategory, SalesByVendor

urlpatterns = [
    path('add-product', AddProductView.as_view()),
    path('edit-product/<int:pk>', EditProductView.as_view()),
    path('delete-product/<int:pk>', DeleteProductView.as_view()),
    
    path('add-category', AddCategoryView.as_view()),
    path('edit-category/<int:pk>', EditCategoryView.as_view()),
    path('delete-category/<int:pk>', DeleteCategoryView.as_view()),
    
    path('sales-category', SalesByCategory.as_view()),
    path('sales-vendor', SalesByVendor.as_view()),
]