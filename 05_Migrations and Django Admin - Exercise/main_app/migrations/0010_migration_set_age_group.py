# Generated by Django 5.0.4 on 2024-06-26 20:24

from django.db import migrations


def set_age_group(apps, schema_editor):
    person_model = apps.get_model('main_app', 'Person')
    all_persons = person_model.objects.all()

    for person in all_persons:
        if person.age <= 12:
            person.age_group = 'Child'
        elif person.age <= 17:
            person.age_group = 'Teen'
        else:
            person.age_group = 'Adult'

        person_model.objects.bulk_update(all_persons, ['age_group'])


def set_age_group_to_default(apps, schema_editor):
    person_model = apps.get_model('main_app', 'Person')

    all_persons = person_model.objects.all()

    for person in all_persons:
        person.age_group = person_model._meta.get_field('age_group').default

    person_model.objects.bulk_update(all_persons, ['age_group'])


class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0009_person'),
    ]

    operations = [
        migrations.RunPython(set_age_group, set_age_group_to_default),
    ]
