from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    orders_count = serializers.SerializerMethodField()
    wishlist_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'profile', 'orders_count', 'wishlist_count']

    def get_orders_count(self, obj):
        return obj.orders.count()

    def get_wishlist_count(self, obj):
        return obj.profile.wishlist.count()