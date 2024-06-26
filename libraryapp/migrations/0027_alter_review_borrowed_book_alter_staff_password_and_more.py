# Generated by Django 5.0.2 on 2024-04-04 04:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0026_alter_staff_password_alter_student_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='borrowed_book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='libraryapp.borrowedbook'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='password',
            field=models.CharField(default='aU51mMGwlkCB', max_length=10, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(default='w0wfKfQPW1mP', max_length=10, verbose_name='Password'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=100)),
                ('payment_status', models.CharField(max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('borrowed_book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='libraryapp.borrowedbook')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='libraryapp.student')),
            ],
        ),
    ]
