from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'first_name', 'last_name', 'email', 
            'address', 'postal_code', 'city', 'total_paid', 'status', 'created_at', 'items'
        ]
        extra_kwargs = {
            'user': {'read_only': True, 'required': False}
        }

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            # Vérification et mise à jour du stock
            if product.stock >= quantity:
                product.stock -= quantity
                product.save()
            else:
                raise serializers.ValidationError(f"Stock insuffisant pour {product.name}")
                
            OrderItem.objects.create(order=order, **item_data)
            
        return order