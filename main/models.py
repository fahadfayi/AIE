from django.db import models

# Create your models here.


class SpaceXLaunch(models.Model):
    flight_number = models.CharField(verbose_name="Flight Number", max_length=16,blank=False)
    date = models.DateField(verbose_name="Date", blank=False)
    time = models.TimeField(verbose_name="Time", blank=False)
    booster_version = models.CharField(verbose_name="Booster Version", max_length=128,blank=False)
    launch_site = models.CharField(verbose_name="Launch Site", max_length=64,blank=False)
    payload = models.CharField(verbose_name="Payload", max_length=256,blank=False)
    payload_weight = models.CharField(verbose_name="Payload Weight", max_length=256,blank=True)
    orbit = models.CharField(verbose_name="Orbit", max_length=128,blank=False)
    customer = models.CharField(verbose_name="Customer", max_length=256,blank=False)
    mission_result = models.CharField(verbose_name="Mission Result", max_length=256,blank=False)
    landing_result = models.CharField(verbose_name="Landing Result", max_length=256,blank=False)
