# Generated by Django 5.0.2 on 2024-03-16 05:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0024_alter_staff_password_alter_student_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='returnedbook',
            name='book',
        ),
        migrations.AddField(
            model_name='returnedbook',
            name='borrowed_book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='libraryapp.borrowedbook'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='password',
            field=models.CharField(default='72GJKxK9mRjU', max_length=10, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(default='5j8DGhPAjiVr', max_length=10, verbose_name='Password'),
        ),
    ]
