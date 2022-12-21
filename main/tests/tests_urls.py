from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import UploadCSVView
from main.views import SpaceXLaunchView

class TestURLs(SimpleTestCase): 

    def test_view_data_url(self):
        url = reverse('view-data')
        self.assertEquals(resolve(url).func.view_class, SpaceXLaunchView)

    def test_upload_csv_url(self):
        url = reverse("upload-csv-file")
        self.assertEquals(resolve(url).func.view_class, UploadCSVView)