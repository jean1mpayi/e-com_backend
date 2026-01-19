from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta
from products.models import Product
from orders.models import Order

class DashboardStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 1. Revenu Total (Commandes payées/livrées)
        # On suppose que toutes les commandes créées sont valides pour ce MVP
        total_revenue = Order.objects.aggregate(
            total=Sum('total_paid')
        )['total'] or 0

        # 2. Total Commandes
        total_orders = Order.objects.count()

        # 3. Total Produits
        total_products = Product.objects.count()

        # 4. Alertes Stock Faible (< 5)
        low_stock_count = Product.objects.filter(stock__lt=5).count()

        return Response({
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "total_products": total_products,
            "low_stock_count": low_stock_count
        })

class DashboardChartView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)

        # Grouper les commandes par jour
        daily_revenue = Order.objects.filter(
            created_at__gte=start_date
        ).annotate(
            date=TruncDay('created_at')
        ).values('date').annotate(
            desktop=Sum('total_paid'), # On utilise 'desktop' pour mapper avec le chart frontend facilement
        ).order_by('date')
        
        # Formater pour le frontend: [{date: "2024-01-01", desktop: 150, mobile: 0}, ...]
        data = []
        for entry in daily_revenue:
            data.append({
                "date": entry['date'].strftime("%Y-%m-%d"),
                "desktop": entry['desktop'] or 0,
                "mobile": 0 # Pas de distinction mobile/desktop dans ce MVP
            })

        return Response(data)
