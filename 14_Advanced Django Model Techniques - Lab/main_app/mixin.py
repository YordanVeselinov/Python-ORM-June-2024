from django.core.validators import MaxValueValidator
from django.db import models


class ReviewMixin(models.Model):
    class Meta:
        abstract = True
        ordering = ['-rating']

    review_content = models.TextField()

    rating = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(5)
        ]
    )

