from django.db import models


class PropertyTypeChoices(models.TextChoices):
    HOUSE = 'House', 'House'
    FLAT = 'Flat', 'Flat'
    VILLA = 'Villa', 'Villa'
    COTTAGE = 'Cottage', 'Cottage'
    STUDIO = 'Studio', 'Studio'


class GenreChoices(models.TextChoices):
    ACTION = 'Action', 'Action'
    RPG = 'RPG', 'RPG'
    ADVENTURE = 'Adventure', 'Adventure'
    SPORTS = 'Sports', 'Sports'
    STRATEGY = 'Strategy', 'Strategy'


class PriorityChoices(models.TextChoices):
    LOW = 'Low', 'Low'
    MEDIUM = 'Medium', 'Medium'
    HIGH = 'High', 'High'
