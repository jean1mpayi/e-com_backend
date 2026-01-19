from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} # Génère le slug automatiquement en tapant le nom

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'is_active', 'is_trending']
    list_filter = ['is_active', 'category', 'is_trending']
    list_editable = ['price', 'stock', 'is_active', 'is_trending']
    prepopulated_fields = {'slug': ('name',)}