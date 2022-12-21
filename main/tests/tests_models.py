from django.test import TestCase
from main.models import SpaceXLaunch
from django.core.exceptions import ValidationError
from django.db import transaction
import datetime
from django.db.utils import IntegrityError

class TestModels(TestCase):

    def setUp(self):
        now = datetime.datetime.now()
        self.current_time = now.strftime("%H:%M:%S") 
        self.today = datetime.date.today()
        spacex = SpaceXLaunch.objects.create(
                        flight_number='test flight name',
                        date=self.today,
                        time=self.current_time,
                        booster_version='test booster',
                        launch_site= 'test Launch Site',
                        payload= 'test Payload',
                        payload_weight= 'test Payload Mass (kg)',
                        orbit= 'test Orbit',
                        customer= 'test Customer',
                        mission_result= 'test Mission Outcome',
                        landing_result= 'test Landing Outcome',
                    )

    def test_date_with_wrong_value(self):
        try:
            with transaction.atomic():
                spacex = SpaceXLaunch(
                        flight_number='test flight name',
                        date='test date',
                        time=self.current_time,
                        booster_version='test booster',
                        launch_site= 'test Launch Site',
                        payload= 'test Payload',
                        payload_weight= 'test Payload Mass (kg)',
                        orbit= 'test Orbit',
                        customer= 'test Customer',
                        mission_result= 'test Mission Outcome',
                        landing_result= 'test Landing Outcome',
                    )
                spacex.save()
        except ValidationError:
            pass
        self.assertEquals(SpaceXLaunch.objects.all().count(), 1)

    def test_time_with_wrong_value(self):
        try:
            with transaction.atomic():
                spacex = SpaceXLaunch(
                        flight_number='test flight name',
                        date=self.today,
                        time='test time',
                        booster_version='test booster',
                        launch_site= 'test Launch Site',
                        payload= 'test Payload',
                        payload_weight= 'test Payload Mass (kg)',
                        orbit= 'test Orbit',
                        customer= 'test Customer',
                        mission_result= 'test Mission Outcome',
                        landing_result= 'test Landing Outcome',
                    )
                spacex.save()
        except ValidationError:
            pass
        self.assertEquals(SpaceXLaunch.objects.all().count(), 1)

    def test_required_with_empty(self):
        try:
            with transaction.atomic():
                spacex = SpaceXLaunch(
                        payload_weight= 'test Payload Mass (kg)',
                    )
                spacex.save()
        except IntegrityError:
            pass
        self.assertEquals(SpaceXLaunch.objects.all().count(), 1)

    def test_nullable_value(self):
        spacex = SpaceXLaunch(
                flight_number='test flight name',
                date=self.today,
                time=self.current_time,
                booster_version='test booster',
                launch_site= 'test Launch Site',
                payload= 'test Payload',
                orbit= 'test Orbit',
                customer= 'test Customer',
                mission_result= 'test Mission Outcome',
                landing_result= 'test Landing Outcome',
            )
        spacex.save()
        self.assertEquals(SpaceXLaunch.objects.all().count(), 2)
