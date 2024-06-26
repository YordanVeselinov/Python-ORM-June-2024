# Generated by Django 5.0.4 on 2024-06-25 13:08
import random

from django.db import migrations


def generate_barcode(apps, schema_editor):
    product = apps.get_model('main_app', 'Product')
    all_products = product.objects.all()
    all_barcodes = random.sample(range(100000000, 1000000000), len(all_products))
    for idx in range(len(all_products)):
        product = all_products[idx]
        product.barcode = all_barcodes[idx]
        product.save()


def reverse_generate_barcode(apps, schema_editor):
    product = apps.get_model('main_app', 'Product')
    for product in product.objects.all():
        product.barcode = 0
        product.save()


class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0004_product_barcode'),
    ]

    operations = [
        migrations.RunPython(generate_barcode, reverse_generate_barcode),
    ]
