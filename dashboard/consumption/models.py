# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class MeterUser(models.Model):
    """A model for users of meters."""

    id = models.IntegerField(primary_key=True)
    area = models.CharField(max_length=16)
    tariff = models.CharField(max_length=16)

    # Cache results of aggregate functions. Remember to update cache after modifying ConsumptionEntries.
    cache_max = models.DecimalField(max_digits=30, decimal_places=3)
    cache_avg = models.DecimalField(max_digits=30, decimal_places=3)

    def cache_update(self):
        self.cache_max = self.consumptionentry_set.aggregate(models.Max('consumption'))['consumption__max']
        self.cache_avg = self.consumptionentry_set.aggregate(models.Avg('consumption'))['consumption__avg']
        self.save()


class ConsumptionEntry(models.Model):
    """A model for readings of meters."""

    user = models.ForeignKey(MeterUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    consumption = models.DecimalField(max_digits=20, decimal_places=3)
