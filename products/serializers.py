from rest_framework import serializers
from .models import Product, Category, Review
from rest_framework.decorators import api_view
from rest_framework.response import Response

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    # Pour la lecture (GET)
    category_details = CategorySerializer(source='category', read_only=True)
    # Pour l'écriture (POST/PUT), on attend un ID
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'category', 'category_details', 'name', 'slug', 
            'description', 'price', 'stock', 
            'image', 'is_active', 'created_at', 'reviews'
        ]


@api_view(['GET'])
def trending_products(request):
    products = Product.objects.filter(is_trending=True)[:4] # On en prend 4 par exemple
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)