from django.db import models
from django.db.models import QuerySet, Count


class TennisPlayerManager(models.Manager):
    def get_tennis_players_by_wins_count(self) -> QuerySet:
        return self.annotate(
            wins=Count('winner')
        ).order_by(
            '-wins',
            'full_name'
        )