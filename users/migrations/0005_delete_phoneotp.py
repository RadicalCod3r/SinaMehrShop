# Generated by Django 4.0.3 on 2022-07-28 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_phoneotp_count'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PhoneOTP',
        ),
    ]
