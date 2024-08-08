from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, RegexValidator
from django.db import models

from main_app.choices import StatusChoices
from main_app.managers import AstronautManager
from main_app.validators import only_digits_phone_number


# Create your models here.
class BaseModel(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ]
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class LaunchDateBase(models.Model):
    class Meta:
        abstract = True

    launch_date = models.DateField()


class Astronaut(BaseModel):
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            RegexValidator(r'^\+359\d{0,11}$')
        ]
    )

    is_active = models.BooleanField(
        default=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    spacewalks = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
        ]
    )

    objects = AstronautManager()


class Spacecraft(BaseModel, LaunchDateBase):
    manufacturer = models.CharField(
        max_length=100,
    )

    capacity = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )

    weight = models.FloatField(
        validators=[
            MinValueValidator(0.0)
        ]
    )


class Mission(BaseModel, LaunchDateBase):
    description = models.TextField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=9,
        choices=StatusChoices.choices,
        default=StatusChoices.PLANNED
    )

    spacecraft = models.ForeignKey(
        to=Spacecraft,
        on_delete=models.CASCADE,
        related_name='missions',
    )

    astronauts = models.ManyToManyField(
        to=Astronaut,
        related_name='missions',
    )

    commander = models.ForeignKey(
        to=Astronaut,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commander'
    )
