from django import forms
from .models import Post, Brand
from influencer.models import Applicant

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_name', 'detail', 'budget', 'max_influencer']
        widgets = {
            'post_name': forms.TextInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'budget': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_influencer': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = [
            'efficiency_prob', 'ads_file', 'url', 'amount', 'summary', 'remarks'
        ]
        widgets = {
            'efficiency_prob': forms.NumberInput(attrs={'class': 'form-control'}),
            'ads_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        

class BrandProfileForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name', 'brand_niche']
        widgets = {
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_niche': forms.Select(attrs={'class': 'form-control'}),
        }