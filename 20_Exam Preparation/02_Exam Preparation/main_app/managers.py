from django.db import models
from django.db.models import QuerySet, Count


class ProfileManager(models.Manager):
    def get_regular_customers(self) -> QuerySet:
        return self.annotate(
            order_count=Count('orders')
        ).filter(
            order_count__gt=2,
        ).order_by('-order_count')
