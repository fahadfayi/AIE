from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.db.models import Q
from main.models import SpaceXLaunch
from django.conf import settings
from main.forms import CSVUploadForm
from main.forms import FilterForm
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
                messages.error(request, "File format is not matching")
                return render(request, self.template_name)
            except AssertionError:
                messages.error(request, "Empty File")
                return render(request, self.template_name)
            return redirect('view-data')
        else:
            messages.error(request, "CSV File is Required")
            return render(request, self.template_name)
    
    def get_csvdata(self, csv_file):
        try:
            df = pd.read_csv(csv_file)
        except UnicodeDecodeError:
            df = pd.DataFrame()
        df = df.fillna(" ")
        if 'Booster Version' in df.columns.values:
            df['Booster Version'] = df['Booster Version'].str.replace('\s+', ' ',regex=True)
        return df

    def add_records(self, df):
        
        for index, row in df.iterrows():
            assert not df.empty
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
        assert not df.empty
        for index, row in df.iterrows():
            SpaceXLaunch.objects.update_or_create(
                flight_number=row['Flight Number'],
                launch_site = row['Launch Site'],
                customer = row['Customer'],
                defaults={
                'date':row['Date'],
                'time':row['Time (UTC)'],
                'booster_version':row['Booster Version'],
                'payload':row['Payload'],
                'payload_weight':row['Payload Mass (kg)'],
                'orbit':row['Orbit'],
                'mission_result':row['Mission Outcome'],
                'landing_result':row['Landing Outcome'],
                    },
            )


class SpaceXLaunchView(ListView):
    template_name = 'show.html'

    def get(self, request):
        if settings.ENABLE_DATATABLE:
            self.template_name = 'show_data_table.html'

        form = FilterForm(request.POST, request.FILES)
        if not form.is_valid():
            messages.error(request,"Filter Value is not Valid")
            return render(request, self.template_name)

        return super().get(request)

    def get_queryset(self):
        query_filter = Q()
        if self.request.GET.get('flight_number'):
            query_filter &= Q(flight_number__icontains = self.request.GET['flight_number'].strip())

        if self.request.GET.get('date_from'):
            query_filter &= Q(date__gte = self.request.GET['date_from'])

        if self.request.GET.get('date_to'):
            query_filter &= Q(date__lte = self.request.GET['date_to'])

        if self.request.GET.get('time_from'):
            query_filter &= Q(time__gte = self.request.GET['time_from'])

        if self.request.GET.get('time_to'):
            query_filter &= Q(time__lte = self.request.GET['time_to'])

        if self.request.GET.get('booster_version'):
            query_filter &= Q(booster_version__icontains = self.request.GET['booster_version'].strip())

        if self.request.GET.get('launch_site'):
            query_filter &= Q(launch_site__icontains = self.request.GET['launch_site'].strip())

        if self.request.GET.get('payload'):
            query_filter &= Q(payload__icontains = self.request.GET['payload'].strip())

        if self.request.GET.get('payload_weight'):
            query_filter &= Q(payload_weight__icontains = self.request.GET['payload_weight'].strip())

        if self.request.GET.get('orbit'):
            query_filter &= Q(orbit__icontains = self.request.GET['orbit'].strip())

        if self.request.GET.get('customer'):
            query_filter &= Q(customer__icontains = self.request.GET['customer'].strip())

        if self.request.GET.get('mission_result'):
            query_filter &= Q(mission_result__icontains = self.request.GET['mission_result'].strip())

        if self.request.GET.get('landing_result'):
            query_filter &= Q(landing_result__icontains = self.request.GET['landing_result'].strip())

        return SpaceXLaunch.objects.filter(query_filter)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quert_params'] = self.request.GET
        return context
        


    
