# Generated by Django 5.0.2 on 2024-02-19 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0011_alter_staff_password_alter_student_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='password',
            field=models.CharField(default='fJyJb7hqTvgD', max_length=10, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(default='jpei21Dd6hx5', max_length=10, verbose_name='Password'),
        ),
    ]
