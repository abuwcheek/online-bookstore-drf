# Generated by Django 5.1.7 on 2025-03-27 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_address_order_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('paid', 'Paid'), ('failed', 'Failed')], default='pending', max_length=20),
        ),
    ]
