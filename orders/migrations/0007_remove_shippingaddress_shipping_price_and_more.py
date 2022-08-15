# Generated by Django 4.0.3 on 2022-08-02 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_rename_paymentmethod_order_payment_method'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='shipping_price',
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_price',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]