from django.core.validators import MinLengthValidator, MinValueValidator, MaxLengthValidator
from django.db import models


class Base(models.Model):
    class Meta:
        abstract = True

    full_name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(120)
        ],
    )

    birth_date = models.DateField(
        default='1900-01-01',
    )

    nationality = models.CharField(
        max_length=50,
        validators=[MaxLengthValidator(50)],
        default='Unknown',
    )

