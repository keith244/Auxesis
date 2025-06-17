from django import forms
from .models import HarvestGroupReport

class HarvestGroupReportForm(forms.ModelForm):
    # Add this field for handling multiple photos
    # photos = forms.FileField(
    #     widget=forms.FileInput(attrs={'multiple': True}),
    #     required=False
    # )
    
    class Meta:
        model = HarvestGroupReport
        fields = ['attendees', 'visitors', 'highlights', 'testimonies', 'offering', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }