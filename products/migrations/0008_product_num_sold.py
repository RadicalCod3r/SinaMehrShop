# Generated by Django 4.0.3 on 2022-07-18 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_productreview_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='num_sold',
            field=models.IntegerField(default=0),
        ),
    ]
