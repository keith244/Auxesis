from django import forms
from .models import HarvestGroupReport, LeadershipApplication

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

class LeadershipApplicationForm(forms.ModelForm):
    role_type = forms.ChoiceField(choices=LeadershipApplication.ROLE_CHOICES)

    target_group_id = forms.IntegerField(
        label="Enter the ID of the target group",
        help_text="For example, the ID of the Harvest Group, Community, or Missional Location."
    )
    
    class Meta:
        model = LeadershipApplication
        fields = ['role_type', 'target_group_id']
