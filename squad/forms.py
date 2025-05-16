from django import forms
from .models import SquadReport

class SquadReportForm(forms.ModelForm):
    # Add this field for handling multiple photos
    # photos = forms.FileField(
    #     widget=forms.FileInput(attrs={'multiple': True}),
    #     required=False
    # )
    
    class Meta:
        model = SquadReport
        fields = ['attendees', 'visitors', 'highlights', 'testimonies', 'offering', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }