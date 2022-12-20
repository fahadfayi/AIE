from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from main.models import SpaceXLaunch
from django.conf import settings
from main.forms import CSVUploadForm
from django.contrib import messages

import pandas as pd
# Create your views here.


class UploadCSVView(TemplateView):
    template_name = 'upload_csv.html'

    def post(self, request):
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            df = self.get_csvdata(form.cleaned_data['csvfile'])
            try:
                self.add_records_no_duplicates(df) if settings.UPDATE_IF_DATA else self.add_records(df)
            except KeyError:
                messages.error(request, "File format not matching")
                return render(request, self.template_name)
            return redirect('view-data')
        else:
            messages.error(request, form.errors.get(
                "csvfile", "Unknown error"))
            return render(request, self.template_name)

    def get_csvdata(self, File):
        csv_file = File
        return pd.read_csv(csv_file)

    def add_records(self, df):
        df = df.fillna(" ")
        for index, row in df.iterrows():
            SpaceXLaunch.objects.create(
                flight_number=row['Flight Number'],
                date=row['Date'],
                time=row['Time (UTC)'],
                booster_version=row['Booster Version'],
                launch_site=row['Launch Site'],
                payload=row['Payload'],
                payload_weight=row['Payload Mass (kg)'],
                orbit=row['Orbit'],
                customer=row['Customer'],
                mission_result=row['Mission Outcome'],
                landing_result=row['Landing Outcome'],
            )

    def add_records_no_duplicates(self, df):
        df = df.fillna(" ")
        for index, row in df.iterrows():
            SpaceXLaunch.objects.update_or_create(
                
                date=row['Date'],
                time=row['Time (UTC)'],
                booster_version=row['Booster Version'],
                payload=row['Payload'],
                payload_weight=row['Payload Mass (kg)'],
                orbit=row['Orbit'],
                mission_result=row['Mission Outcome'],
                landing_result=row['Landing Outcome'],
                defaults={
                        'flight_number':row['Flight Number'],
                        'launch_site': row['Launch Site'],
                        'customer':row['Customer'],
                    },
            )


class SpaceXLaunchView(ListView):
    model = SpaceXLaunch
    template_name = 'show.html'

    def get(self, request):
        if settings.ENABLE_DATATABLE:
            self.template_name = 'show_data_table.html'
        return super().get(request)
