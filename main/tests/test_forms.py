from django.test import TestCase
from main.forms import CSVUploadForm
from main.forms import FilterForm
import datetime
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile


class TestForms(TestCase):

    def setUp(self):
        now = datetime.datetime.now()
        self.current_time = now.strftime("%H:%M:%S") 
        self.today = datetime.date.today()


    def test_form_csv_upload(self):
        with open('main/tests/files/spacex_launch_data.csv', 'rb') as csv_file:
            document = SimpleUploadedFile(csv_file.name, csv_file.read(), content_type='application/csv')
        form = CSVUploadForm(data={},files={'csvfile':document})
        self.assertTrue(form.is_valid())
        self.assertEquals(len(form.errors), 0)

    def test_noncsv_upload(self):
        with open('main/tests/files/sample_text.txt', 'rb') as csv_file:
            document = SimpleUploadedFile(csv_file.name, csv_file.read())
        form = CSVUploadForm(data={},files={'csvfile':document})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_filter_form(self):
        dct_filter = {
            'flight_number' : 'test',
            'date_from' : self.today,
            'date_to' : self.today,
            'time_from' : self.current_time,
            'time_to' : self.current_time,
            'booster_version' : 'test',
            'launch_site' : 'test',
            'payload' : 'test',
            'payload_weight' : 'test',
            'orbit' : 'test',
            'customer' : 'test',
            'mission_result' : 'test',
            'landing_result' : 'test landing'
        }
        form = FilterForm(data = dct_filter)
        self.assertTrue(form.is_valid())

    def test_filter_wrongdata_form(self):
        dct_filter = {
            'flight_number' : 'test',
            'date_from' : 'test',
            'date_to' : 'test',
            'time_from' : 'test',
            'time_to' : 'test',
            'booster_version' : 'test',
            'launch_site' : 'test',
            'payload' : 'test',
            'payload_weight' : 'test',
            'orbit' : 'test',
            'customer' : 'test',
            'mission_result' : 'test',
            'landing_result' : 'test landing'
        }
        form = FilterForm(data = dct_filter)
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_filter_skipdata_form(self):
        dct_filter = {
            'flight_number' : 'test',
            'time_to' : self.current_time,
            'booster_version' : 'test',
            'launch_site' : 'test',
            'payload' : 'test',
            'payload_weight' : 'test',
            'customer' : 'test',
            'mission_result' : 'test',
            'landing_result' : 'test landing'
        }
        form = FilterForm(data = dct_filter)
        self.assertTrue(form.is_valid())