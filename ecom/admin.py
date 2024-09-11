from django.contrib import admin
from .models import Product, Category, Cart, CartItem

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'price',
        'stock',
        'available',
        'created',
        'updated',
    ]
    list_editable = ['price', 'stock', 'available',]
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 5
admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
    ]
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)

