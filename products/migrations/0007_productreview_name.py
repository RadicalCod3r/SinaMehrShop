# Generated by Django 4.0.3 on 2022-07-18 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_productreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='name',
            field=models.CharField(default='کاربر جدید', max_length=50),
        ),
    ]
