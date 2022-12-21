from django.test import TestCase, Client
from django.urls import reverse
from main.models import SpaceXLaunch
from django.conf import settings


import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_add_csv_GET(self):
        response = self.client.get(reverse('upload-csv-file'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload_csv.html')

    def test_view_data_GET(self):
        response = self.client.get(reverse('view-data'))
        self.assertEquals(response.status_code, 200)
        if settings.ENABLE_DATATABLE:
            self.assertTemplateUsed(response, 'show_data_table.html')
        else:
            self.assertTemplateUsed(response, 'show.html')


    def test_add_csv_POST_no_data(self):
        response = self.client.post(reverse('upload-csv-file'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload_csv.html')
        self.assertEquals(SpaceXLaunch.objects.filter().count(), 0)

    def test_add_csv_POST_other_file(self):
        with open('main/tests/files/sample.csv') as csv_file:
            response = self.client.post(reverse('upload-csv-file'), {'csvfile':csv_file})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(SpaceXLaunch.objects.filter().count(), 0)

    def test_add_csv_POST_orignal_file(self):
        with open('main/tests/files/spacex_launch_data.csv') as csv_file:
            response = self.client.post(reverse('upload-csv-file'), {'csvfile':csv_file})
        self.assertEquals(response.status_code, 302)
        
        self.assertNotEquals(SpaceXLaunch.objects.filter().count(), 0)

    def test_view_data_filter(self):
        response = self.client.get(reverse('view-data'),{'flight_number':'2'})
        self.assertEquals(response.status_code, 200)
        if settings.ENABLE_DATATABLE:
            self.assertTemplateUsed(response, 'show_data_table.html')
        else:
            self.assertTemplateUsed(response, 'show.html')
