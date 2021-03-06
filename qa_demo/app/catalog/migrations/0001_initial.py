# Generated by Django 3.1.5 on 2021-01-30 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Producto')),
                ('link', models.URLField(verbose_name='Link de Producto')),
                ('clasification', models.CharField(max_length=255, verbose_name='Clasificación')),
                ('product_type', models.CharField(max_length=255, verbose_name='Tipo')),
                ('brand', models.CharField(blank=True, max_length=255, null=True, verbose_name='Marca')),
                ('vendor_link', models.URLField(blank=True, null=True, verbose_name='')),
                ('vendor_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Vendedor')),
                ('vendor_sales', models.CharField(max_length=255, verbose_name='Ventas')),
                ('vendor_location', models.CharField(max_length=255, verbose_name='Ubicación')),
            ],
            options={
                'db_table': 'product_catalog',
                'ordering': ('name',),
            },
        ),
    ]
