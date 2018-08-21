from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

import csv
import decimal
import os
import sys

from consumption.models import MeterUser, ConsumptionEntry


class Command(BaseCommand):
    help = 'import data'

    def handle(self, *args, **options):
        # TODO: Add an option to open data in a different directory.
        # Ensure that the command works even if not called from the project directory
        script_directory = os.path.dirname(os.path.realpath(sys.argv[0]))

        # Using os.path.join to ensure portability
        try:
            users_csv = open(os.path.join(script_directory, "..", "data", "user_data.csv"), "r")
        except FileNotFoundError:
            raise CommandError("user_data.csv not found.")

        users_reader = csv.reader(users_csv)

        header = next(users_reader)
        if header != ["id", "area", "tariff"]:
            raise CommandError("Invalid user_data.csv header.")

        for row in users_reader:
            try:
                user_id = int(row[0])
            except ValueError:
                print("Invalid user ID %s. Skipping." % row[0], file=sys.stderr)

            print("Processing user %d." % user_id)

            try:
                consumption_csv = open(os.path.join(script_directory, "..", "data", "consumption", "%d.csv" % user_id),
                                       "r")
            except FileNotFoundError:
                print("Consumption file for user %d not found. Skipping." % user_id, file=sys.stderr)

            try:
                with transaction.atomic():
                    user = MeterUser.objects.get_or_create(id=user_id, area=row[1], tariff=row[2])[0]

                    consumption_reader = csv.reader(consumption_csv)
                    if next(consumption_reader) != ["datetime", "consumption"]:
                        raise ValueError

                    # Make sure that datetimes are unique for any given user.
                    # In case an entry already exists, overwrite it.

                    for reading in consumption_reader:
                        current_tz = timezone.get_current_timezone()
                        reading_date = timezone.datetime.strptime(reading[0], "%Y-%m-%d %H:%M:%S")
                        reading_date = current_tz.localize(reading_date)

                        reading_value = decimal.Decimal(reading[1])

                        try:
                            consumption = ConsumptionEntry.objects.get(user=user, datetime=reading_date)
                            consumption.consumption = reading_value
                            consumption.save()
                        except ConsumptionEntry.DoesNotExist:
                            consumption = ConsumptionEntry(user=user, datetime=reading_date, consumption=reading_value)
                            consumption.save()

            except ValueError:
                print("CSV file for user %d is malformed. Roll-backed changes." % user_id, file=sys.stderr)

        print("Finished!")
