from django import forms
from main.models import UploadedFile


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
