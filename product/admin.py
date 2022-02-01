from django.contrib import admin
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','price']
    search_fields = ( 'title','category_title',)
    list_per_page = 20


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    search_fields = ( 'title',)


admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)