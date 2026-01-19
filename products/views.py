from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

# products/views.py

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'name']
    
    # Pour accepter l'upload d'images
    from rest_framework.parsers import MultiPartParser, FormParser
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'trending']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        # Admin voit tout, les autres seulement les actifs
        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset = Product.objects.all()
        else:
            queryset = Product.objects.filter(is_active=True)
        
        # 1. Filtrage par SLUG (utilisé pour ton menu de navigation)
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # 2. Filtrage par ID (utilisé pour les produits similaires)
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
            
        return queryset

    @action(detail=False, methods=['get'])
    def trending(self, request):
        products = Product.objects.filter(is_active=True, is_trending=True)[:4]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='top-selling')
    def top_selling(self, request):
        from django.db.models import Count
        products = Product.objects.annotate(
            total_orders=Count('order_items')
        ).order_by('-total_orders')[:10]
        
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]