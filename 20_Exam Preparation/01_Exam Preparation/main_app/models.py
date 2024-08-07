from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxLengthValidator, MaxValueValidator
from main_app.base_models import Base
from main_app.choices import GenreChoices
from main_app.managers import DirectorManager
from main_app.mixins import IsAwardedMixin, LastUpdatedMixin


# Create your models here.
class Director(Base):
    years_of_experience = models.SmallIntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )

    objects = DirectorManager()


class Actor(Base, IsAwardedMixin, LastUpdatedMixin):
    pass


class Movie(IsAwardedMixin, LastUpdatedMixin):
    title = models.CharField(
        max_length=150,
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(150),
        ]
    )

    release_date = models.DateField()

    storyline = models.TextField(
        null=True,
        blank=True,
    )

    genre = models.CharField(
        max_length=20,
        choices=GenreChoices.choices,
        default=GenreChoices.OTHER,
        validators=[
            MinLengthValidator(6),
        ]
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(10.0),
        ]
    )

    is_classic = models.BooleanField(
        default=False,
    )

    director = models.ForeignKey(
        to=Director,
        on_delete=models.CASCADE,
        related_name='director_movies',
    )

    starring_actor = models.ForeignKey(
        to=Actor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='starring_actor_movies',
    )

    actors = models.ManyToManyField(
        to=Actor,
        related_name='actor_movies',
    )

