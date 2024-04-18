# Generated by Django 5.0.2 on 2024-04-06 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0028_payment_currency_payment_razorpay_order_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='razorpay_order_id',
        ),
        migrations.AlterField(
            model_name='staff',
            name='password',
            field=models.CharField(default='vB3xxT1Rycth', max_length=10, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(default='2SPFq4NQ7tWs', max_length=10, verbose_name='Password'),
        ),
    ]
