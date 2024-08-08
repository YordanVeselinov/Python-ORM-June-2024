import os
import django
from django.db.models import Q, Count, Sum, Avg, F

from main_app.choices import StatusChoices
from main_app.populate_db import populate_model_with_data

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut, Spacecraft, Mission


# Create queries within functions
def get_astronauts(search_string=None) -> str:
    if search_string is None:
        return ''

    astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string)
        |
        Q(phone_number__icontains=search_string)
    ).order_by(
        'name'
    )

    if not astronauts:
        return ''

    result = []

    for a in astronauts:
        result.append(
            f'Astronaut: {a.name}, phone number: {a.phone_number}, status: {"Active" if a.is_active else "Inactive"}')

    return '\n'.join(result)


def get_top_astronaut() -> str:
    top_astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()

    if not top_astronaut or top_astronaut.missions_count == 0:
        return 'No data.'

    return f'Top Astronaut: {top_astronaut.name} with {top_astronaut.missions_count} missions.'


def get_top_commander() -> str:
    top_commander = Astronaut.objects.annotate(
        commander_count=Count('commander')
    ).order_by(
        '-commander_count',
        'phone_number'
    ).first()

    if not top_commander or top_commander.commander_count == 0:
        return 'No data.'

    return f'Top Commander: {top_commander.name} with {top_commander.commander_count} commanded missions.'


def get_last_completed_mission() -> str:
    mission = Mission.objects.select_related(
        'spacecraft',
    ).prefetch_related(
        'astronauts',
    ).annotate(
        spacewalks=Sum('astronauts__spacewalks'),
    ).filter(
        status=StatusChoices.COMPLETED,
    ).order_by(
        '-launch_date'
    ).first()

    if not mission:
        return 'No data.'

    commander = mission.commander.name if mission.commander else 'TBA'
    astronauts = ', '.join(mission.astronauts.order_by('name').values_list('name', flat=True))
    spacewalks = mission.spacewalks

    return f'The last completed mission is: {mission.name}. ' \
           f'Commander: {commander}. ' \
           f'Astronauts: {astronauts}. ' \
           f'Spacecraft: {mission.spacecraft.name}. ' \
           f'Total spacewalks: {spacewalks}.'


def get_most_used_spacecraft() -> str:
    most_used_spacecraft = Spacecraft.objects.annotate(
        mission_count=Count('missions'),
    ).order_by(
        '-mission_count',
        'name'
    ).first()

    if not most_used_spacecraft or most_used_spacecraft.mission_count == 0:
        return 'No data.'

    unique_astronauts = Astronaut.objects.filter(
        missions__spacecraft=most_used_spacecraft
    ).distinct().count()

    return f'The most used spacecraft is: {most_used_spacecraft.name}, ' \
           f'manufactured by {most_used_spacecraft.manufacturer}, ' \
           f'used in {most_used_spacecraft.mission_count} missions, ' \
           f'astronauts on missions: {unique_astronauts}.'


def decrease_spacecrafts_weight() -> str:
    spacecrafts = Spacecraft.objects.filter(
        missions__status=StatusChoices.PLANNED,
        weight__gte=200.0
    ).distinct()

    spacecraft_count = spacecrafts.update(
        weight=F('weight') - 200
    )

    if spacecraft_count == 0:
        return 'No changes in weight.'

    avg_weight = Spacecraft.objects.aggregate(
        avg_weight=Avg('weight')
    )

    return f'The weight of {spacecraft_count} spacecrafts has been decreased. ' \
           f'The new average weight of all spacecrafts is {avg_weight["avg_weight"]:.1f}kg'


print(decrease_spacecrafts_weight())