"""
items/forms.py — Item creation and editing forms.
"""

from django import forms
from .models import Item


TAILWIND_INPUT = (
    'w-full px-4 py-3 rounded-xl border border-slate-200 bg-white '
    'focus:outline-none focus:ring-2 focus:ring-indigo-400 text-slate-800 text-sm'
)

TAILWIND_SELECT = (
    'w-full px-4 py-3 rounded-xl border border-slate-200 bg-white '
    'focus:outline-none focus:ring-2 focus:ring-indigo-400 text-slate-800 text-sm cursor-pointer'
)


class ItemForm(forms.ModelForm):
    class Meta:
        model  = Item
        fields = ['title', 'description', 'category', 'item_type', 'date_of_incident', 'location', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. Blue Boat shoes'}),
            'description': forms.Textarea(attrs={
                'class': TAILWIND_INPUT, 'rows': 4,
                'placeholder': 'Describe the item in detail — colour, brand, distinguishing marks…',
            }),
            'category': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'item_type': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'date_of_incident': forms.DateInput(attrs={'class': TAILWIND_INPUT, 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. Library 2nd floor'}),
        }
        labels = {
            'item_type': 'Type',
            'date_of_incident': 'Date Lost / Found',
        }


class SearchForm(forms.Form):
    q        = forms.CharField(required=False, label='Search',
                    widget=forms.TextInput(attrs={
                        'class': TAILWIND_INPUT,
                        'placeholder': 'Search items…',
                    }))
    category = forms.ChoiceField(required=False, choices=[('', 'All Categories')] + Item.CATEGORY_CHOICES,
                    widget=forms.Select(attrs={'class': TAILWIND_SELECT}))
    location = forms.CharField(required=False,
                    widget=forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'Location'}))
    item_type = forms.ChoiceField(required=False,
                    choices=[('', 'Lost & Found'), ('LOST', 'Lost'), ('FOUND', 'Found')],
                    widget=forms.Select(attrs={'class': TAILWIND_SELECT}))
