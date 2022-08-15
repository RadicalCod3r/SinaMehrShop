from rest_framework import serializers
from .models import (
    OrderItem,
    ShippingAddress,
    Order
)
from users.serializers import UserSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'name', 'image', 'price', 'qty')


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ('province', 'city', 'address', 'postal_code')


class OrderSerializer(serializers.ModelSerializer):
    orders = serializers.SerializerMethodField(read_only=True)
    shipping_address = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_orders(self, obj):
        order_items = obj.order_items.all()
        serializer = OrderItemSerializer(order_items, many=True)
        return serializer.data

    def get_shipping_address(self, obj):
        serializer = ShippingAddressSerializer(obj.shipping_address, many=False)
        return serializer.data

    def get_user(self, obj):
        serializer = UserSerializer(obj.user, many=False)
        return serializer.data