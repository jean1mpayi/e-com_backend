from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # On ne retourne que les commandes de l'utilisateur connecté
        return Order.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # On lie automatiquement le user connecté à la commande
        serializer.save(user=self.request.user)