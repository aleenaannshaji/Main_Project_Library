# Generated by Django 5.0.2 on 2024-02-19 07:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0010_borrowedbook_fine_amount_alter_staff_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='password',
            field=models.CharField(default='0QVm3OvJvsaJ', max_length=10, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(default='TONAcwC4ahKW', max_length=10, verbose_name='Password'),
        ),
        migrations.CreateModel(
            name='BookRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libraryapp.student')),
            ],
        ),
    ]
