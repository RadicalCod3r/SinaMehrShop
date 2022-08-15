from django.db import models
from users.models import User
from products.models import Product

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    shipping_price = models.CharField(max_length=10, null=True, blank=True)
    total = models.CharField(max_length=10, null=False, blank=False)
    payment_method = models.CharField(max_length=200, default='زرین پال', null=False, blank=False)
    shipping_method = models.CharField(max_length=200, default='پست پیشتاز', null=False, blank=False)
    is_paid = models.BooleanField(default=False, null=False, blank=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    id_delivered = models.BooleanField(default=False, null=False, blank=False)
    deliver_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.name} {self.created_at}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False, blank=False)
    qty = models.PositiveIntegerField(default=1)
    price = models.CharField(max_length=10, null=False, blank=False)
    image = models.ImageField(upload_to='images/products')

    def __str__(self):
        return f'{self.qty} {self.product}'


class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping_address')
    province = models.CharField(max_length=200, null=False, blank=False)
    city = models.CharField(max_length=200, null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    postal_code = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return f'{self.province}, {self.city}, {self.address}'
