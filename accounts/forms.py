from django import forms

class AccountSettingsForm(forms.Form):
    organization = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=100, required=False,
                            label="Phone # (optional)")
