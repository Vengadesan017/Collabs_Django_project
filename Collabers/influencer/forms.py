from django import forms
from .models import Applicant

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant

        fields = [
            'post','influencer','efficiency_prob', 'ads_file', 'url', 'amount', 'summary', 'remarks'
        ]
        widgets = {
            'efficiency_prob': forms.NumberInput(attrs={'class': 'form-control'}),
            'ads_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }