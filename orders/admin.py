from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    """Permet d'afficher les produits directement dans la fiche commande"""
    model = OrderItem
    raw_id_fields = ['product'] # Affiche l'ID pour éviter de charger une liste déroulante immense
    extra = 0 # N'affiche pas de lignes vides par défaut

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Liste des colonnes affichées dans le tableau général
    list_display = [
        'id', 'first_name', 'last_name', 'email', 
        'address', 'postal_code', 'city', 'total_paid', 
        'created_at', 'updated_at'
    ]
    
    # Filtres sur le côté droit
    list_filter = ['created_at', 'updated_at', 'city']
    
    # Barre de recherche
    search_fields = ['first_name', 'last_name', 'email', 'address']
    
    # Ajout des produits à l'intérieur de la commande
    inlines = [OrderItemInline]
    
    # Optionnel : trier par date de création décroissante
    ordering = ['-created_at']

# Si tu veux aussi pouvoir voir les items séparément (optionnel)
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'price', 'quantity']
    list_filter = ['product']