# Generated by Django 5.0.2 on 2024-03-16 03:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0021_bookrequest_no_of_copies_alter_staff_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='password',
            field=models.CharField(default='ffS6MbEwmWM7', max_length=10, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(default='7aunrm4EF2No', max_length=10, verbose_name='Password'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('borrowed_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libraryapp.borrowedbook')),
            ],
        ),
    ]