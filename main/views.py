from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from main.models import SpaceXLaunch
from django.conf import settings

import pandas as pd
# Create your views here.


class UploadCSVView(TemplateView):
    template_name = 'upload_csv.html'

    def post(self, request):
        df = self.get_csvdata(request)
        self.add_records(df)
        return redirect('view-data')

    def get_csvdata(self,request):
        csv_file = request.FILES['csv-file']
        return pd.read_csv(csv_file)

    def add_records(self, df):
        df = df.fillna(" ")
        for index,row in df.iterrows():
            SpaceXLaunch.objects.create(
                flight_number = row['Flight Number'],
                date = row['Date'],
                time = row['Time (UTC)'],
                booster_version = row['Booster Version'],
                launch_site = row['Launch Site'],
                payload = row['Payload'],
                payload_weight = row['Payload Mass (kg)'],
                orbit = row['Orbit'],
                customer = row['Customer'],
                mission_result = row['Mission Outcome'],
                landing_result = row['Landing Outcome'],
            )

class SpaceXLaunchView(ListView):
    model = SpaceXLaunch
    template_name = 'show.html'
    
    def get(self, request):
        if settings.ENABLE_DATA_TABLE:
            self.template_name = 'show_data_table.html'
        return super().get(request)
