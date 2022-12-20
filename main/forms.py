from django import forms

def validate_file_extension(value):
        if not value.name.endswith('.csv'):
            raise forms.ValidationError("Only CSV file is accepted")

class CSVUploadForm(forms.Form):
    csvfile = forms.FileField(validators=[validate_file_extension])

