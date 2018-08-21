# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.db.utils import IntegrityError

from consumption.models import MeterUser, ConsumptionEntry


class ModelTest(TestCase):
    def setUp(self):
        pass

    def test_create_user(self):
        MeterUser.objects.create(id=500, area="Gdynia", tariff="udręka13")
        with self.assertRaises(IntegrityError):
            MeterUser.objects.create(id=500, area="Gdańsk", tariff="udręka14")


