# Generated by Django 5.0.4 on 2024-06-26 20:42

from django.db import migrations


def set_rarity_of_items(apps, schema_editor):
    item_model = apps.get_model('main_app', 'Item')

    all_items = item_model.objects.all()

    for item in all_items:
        if item.price <= 10:
            item.rarity = 'Rare'
        elif item.price <= 20:
            item.rarity = 'Very Rare'
        elif item.price <= 30:
            item.rarity = 'Extremely Rare'
        else:
            item.rarity = 'Mega Rare'

    item_model.objects.bulk_update(all_items, ['rarity'])


def set_rarity_of_items_on_default(apps, schema_editor):
    item_model = apps.get_model('main_app', 'Item')

    all_items = item_model.objects.all()
    for item in all_items:
        item.rarity = item_model._meta.get_field('rarity').default

    item_model.objects.bulk_update(all_items, ['rarity'])


class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0011_item'),
    ]

    operations = [
        migrations.RunPython(set_rarity_of_items, set_rarity_of_items_on_default),
    ]
