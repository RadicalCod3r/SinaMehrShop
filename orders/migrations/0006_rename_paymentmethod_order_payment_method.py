# Generated by Django 4.0.3 on 2022-08-02 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_rename_shippingprice_shippingaddress_shipping_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='paymentMethod',
            new_name='payment_method',
        ),
    ]