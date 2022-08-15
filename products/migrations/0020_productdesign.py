# Generated by Django 4.0.3 on 2022-07-24 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_color_productfamily'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDesign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use', models.CharField(max_length=100)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='family_designs', to='products.productfamily')),
            ],
            options={
                'unique_together': {('family', 'use')},
            },
        ),
    ]
