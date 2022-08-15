from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import (
    OrderItem,
    Order,
    ShippingAddress
)
from .serializers import OrderSerializer
from products.models import Product

# Create your views here.
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated,])
def add_order(request):
    user = request.user
    data = request.data

    order_items = data['order_items']

    if order_items and len(order_items) == 0:
        return Response({'detail': 'شما هنوز هیچ آیتمی را برای خرید انتخاب نکرده اید.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        order = Order.objects.create(
            user=user,
            first_name=data['personal_info']['first_name'],
            last_name=data['personal_info']['last_name'],
            total=data['total']
        )

        shipping_address = ShippingAddress.objects.create(
            order=order,
            province=data['shipping_address']['province'],
            city=data['shipping_address']['city'],
            address=data['shipping_address']['address'],
            postal_code=data['shipping_address']['postal_code']
        )

        for i in order_items:
            product = Product.objects.get(id=i['product'])

            item = OrderItem.objects.create(
                order=order,
                product=product,
                name=product.name,
                price=product.price,
                qty=i['qty'],
                image=product.image
            )

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_order(request, pk):
    user = request.user

    order = Order.objects.filter(id=pk)

    if order.exists():
        order = order.first()

        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response({'detail': 'شما اجازه دسترسی به این سفارش را ندارید.'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'detail': 'چنین سفارشی وجود ندارد.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated,])
def get_my_orders(request):
    user = request.user

    orders = Order.objects.filter(user=user).all()

    if orders.exists():
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    else:
        return Response({'detail': 'شما هیچ سفارشی ندارید.'}, status=status.HTTP_404_NOT_FOUND)