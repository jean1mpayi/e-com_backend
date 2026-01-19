from django.db import models
from django.conf import settings
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('paid', 'Payée'),
        ('shipped', 'Expédiée'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
    )

    user = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
    on_delete=models.CASCADE, 
    related_name='orders',
    null=True,   # Permet de ne pas avoir d'utilisateur lié
    blank=True   # Permet de laisser le champ vide dans l'admin
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Commande {self.id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Prix au moment de l'achat
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)