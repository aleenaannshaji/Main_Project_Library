# Generated by Django 5.0.2 on 2024-02-12 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Student Name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email id')),
                ('password', models.CharField(max_length=50, verbose_name='PAssword')),
            ],
        ),
    ]
