# Generated by Django 5.0.2 on 2024-02-14 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='country'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='full_name',
            field=models.CharField(blank=True, max_length=264, null=True, verbose_name='full name'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='phone'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='state',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='state'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(blank=True, max_length=264, null=True, verbose_name='username'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='zipcode',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='zipcode'),
        ),
    ]