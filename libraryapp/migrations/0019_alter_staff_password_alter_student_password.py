# Generated by Django 5.0.2 on 2024-02-28 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0018_department_designation_staff_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='password',
            field=models.CharField(default='noYJpy4cwX43', max_length=10, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(default='CAyonIGxlq2e', max_length=10, verbose_name='Password'),
        ),
    ]
