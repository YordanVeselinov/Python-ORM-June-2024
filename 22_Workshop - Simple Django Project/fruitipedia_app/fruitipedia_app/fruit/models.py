from django.core.validators import MinLengthValidator
from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
    )


class Fruit(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(
                2,
                message='Fruit name should contain only letters!',
            ),
        ]
    )

    image_url = models.URLField(
        null=False,
        blank=False,
    )

    description = models.TextField(
        null=False,
        blank=False,
    )

    nutrition = models.TextField(
        null=False,
        blank=False,
    )
