from django.db import models


class SurfaceTypeChoices(models.TextChoices):
    GRASS = 'Grass', 'Grass'
    NOT_SELECTED = 'Not Selected', 'Not Selected'
    CLAY = 'Clay', 'Clay'
    HARD_COURT = 'Hard Court', 'Hard Court'