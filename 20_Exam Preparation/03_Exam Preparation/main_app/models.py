from django.core.validators import MaxLengthValidator, MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.choices import CategoryChoices
from main_app.managers import AuthorManager


# Create your models here.

class PublishedOnBase(models.Model):
    class Meta:
        abstract = True

    published_on = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )


class Author(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3),
        ]
    )

    email = models.EmailField(
        unique=True,
    )

    is_banned = models.BooleanField(
        default=False,
    )

    birth_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2005),
        ]
    )

    website = models.URLField(
        null=True,
        blank=True,
    )

    objects = AuthorManager()


class Article(PublishedOnBase):
    title = models.CharField(
        max_length=200,
        validators=[
            MaxLengthValidator(200),
            MinLengthValidator(5),
        ]
    )

    content = models.TextField(
        validators=[
            MinLengthValidator(10),
        ]
    )

    category = models.CharField(
        max_length=10,
        choices=CategoryChoices.choices,
        default=CategoryChoices.TECHNOLOGY,
        validators=[
            MaxLengthValidator(10),
        ]
    )
    authors = models.ManyToManyField(
        to=Author,
        related_name='articles',
    )


class Review(PublishedOnBase):
    content = models.TextField(
        validators=[
            MinLengthValidator(10)
        ]
    )

    rating = models.FloatField(
        validators=[
            MaxValueValidator(5.0),
            MinValueValidator(1.0),
        ]
    )

    author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    article = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
