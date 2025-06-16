from django import forms
from .models import PerformanceBonusRule

class PerformanceBonusRuleForm(forms.ModelForm):
    class Meta:
        model = PerformanceBonusRule
        fields = ['min_score_threshold', 'bonus_amount']
        widgets = {
            'min_score_threshold': forms.NumberInput(attrs={'step': '0.01'}),
            'bonus_amount': forms.NumberInput(attrs={'step': '0.01'}),
        }
