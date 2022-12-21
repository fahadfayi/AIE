from django import forms

def validate_file_extension(value):
        if not value.name.endswith('.csv'):
            raise forms.ValidationError("Only CSV file is accepted")

class CSVUploadForm(forms.Form):
    csvfile = forms.FileField(validators=[validate_file_extension])

class FilterForm(forms.Form):
    flight_number = forms.CharField( required=False)
    date_from = forms.DateField( required=False)
    date_to = forms.DateField(required=False)
    time_from = forms.TimeField(required=False)
    time_to = forms.TimeField( required=False)
    booster_version = forms.CharField(required=False)
    launch_site = forms.CharField(required=False)
    payload = forms.CharField(required=False)
    payload_weight = forms.CharField(required=False)
    orbit = forms.CharField(required=False)
    customer = forms.CharField(required=False)
    mission_result = forms.CharField(required=False)
    landing_result = forms.CharField(required=False)

