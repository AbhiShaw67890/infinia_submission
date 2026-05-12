"""
accounts/forms.py — Authentication and profile forms.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class SignupForm(UserCreationForm):
    email      = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name  = forms.CharField(max_length=30, required=False)
    college    = forms.CharField(max_length=120, required=False, label='College / Institute')

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email', 'college', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 bg-white '
                         'focus:outline-none focus:ring-2 focus:ring-indigo-400 text-slate-800 text-sm',
            })


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 bg-white '
                         'focus:outline-none focus:ring-2 focus:ring-indigo-400 text-slate-800 text-sm',
            })


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email', 'college', 'phone', 'bio', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'avatar':
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 bg-white '
                             'focus:outline-none focus:ring-2 focus:ring-indigo-400 text-slate-800 text-sm',
                })
