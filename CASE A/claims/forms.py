"""
claims/forms.py
"""

from django import forms
from .models import Claim


class ClaimForm(forms.ModelForm):
    class Meta:
        model  = Claim
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 bg-white '
                         'focus:outline-none focus:ring-2 focus:ring-indigo-400 text-slate-800 text-sm',
                'rows': 5,
                'placeholder': 'This item belongs to me because… (describe identifying details, circumstances, etc.)',
            }),
        }
        labels = {'message': 'Your Message'}
