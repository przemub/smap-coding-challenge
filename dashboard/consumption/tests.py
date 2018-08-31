# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.management import call_command
from django.core.management.base import CommandError

from consumption.models import MeterUser, ConsumptionEntry

import io


class ModelTest(TestCase):
    def setUp(self):
        pass

    def test_create_user_same_id(self):
        MeterUser.objects.create(id=500, area="Gdynia", tariff="udręka13")
        with self.assertRaises(IntegrityError):
            MeterUser.objects.create(id=500, area="Gdańsk", tariff="udręka14")


class ImportTest(TestCase):
    def setUp(self):
        pass

    def test_custom_input(self):
        with self.assertRaises(TypeError):
            call_command('import', user_data=1)
        with self.assertRaises(TypeError):
            call_command('import', consumption_csv=1)

    def test_bad_header(self):
        with self.assertRaises(CommandError):
            csv = io.StringIO("2,abc,def\n")
            call_command('import', user_data=csv)

    def test_create_users(self):
        csv = io.StringIO("id,area,tariff\n2,abc,def\n3,ghi,jkl\n4,mno,pqr")
        call_command('import', user_data=csv)



