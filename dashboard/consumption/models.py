# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class MeterUser(models.Model):
    """A model for users of meters."""

    id = models.IntegerField(primary_key=True)
    area = models.CharField(max_length=16)
    tariff = models.CharField(max_length=16)


class ConsumptionEntry(models.Model):
    """A model for readings of meters."""

    user = models.ForeignKey(MeterUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    consumption = models.DecimalField(max_digits=20, decimal_places=3)
