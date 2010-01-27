from django import forms

class AccountSettingsForm(forms.Form):
    username = forms.CharField(max_length=64, label="User Name")
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(max_length=64, label="First Name")
    last_name = forms.CharField(max_length=64, label="Last Name")
    organization = forms.CharField(max_length=200, label="Organization")
    phone = forms.CharField(max_length=100, required=False,
                            label="Phone # (optional)")
    twitter = forms.CharField(max_length=100, required=False,
                              label="Twitter ID (optional)")
