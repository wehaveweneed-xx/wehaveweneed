#!/usr/bin/env python
from django import forms
from wehaveweneed.web.models import *
#from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django.contrib.localflavor.us.forms import *
from registration.forms import RegistrationFormUniqueEmail
from registration.models import RegistrationProfile

class RegistrationForm(RegistrationFormUniqueEmail):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    organization = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=100, required=False,
                            label="Phone # (optional)")

    def save(self, profile_callback=None):
        new_user = RegistrationProfile.objects.create_inactive_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
            email=self.cleaned_data['email'],
            profile_callback=profile_callback)

        new_user.first_name = self.cleaned_data.get('first_name', "")
        new_user.last_name = self.cleaned_data.get('last_name', "")
        new_user.save()

        UserProfile.objects.create(
            user=new_user,
            organization=self.cleaned_data['organization'],
            phone=self.cleaned_data.get('phone', ""))

        return new_user

class AccountSettingsForm(forms.Form):
    organization = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=100, required=False,
                            label="Phone # (optional)")

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'type', 'priority',
                  'location',
                  'category',
                  'content',)

class ReplyForm(forms.Form):
    content = forms.CharField(required=False,
                              widget=forms.Textarea())

class UnauthenticatedReplyForm(ReplyForm):
    email = forms.EmailField()

class userprofileForm(forms.Form):
    username = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'size':'25'}),error_messages={'required': 'Please enter a username'})
    first_name = forms.CharField(initial='',label='First Name',max_length=50,widget=forms.TextInput(attrs={'size':'25'}),error_messages={'required': 'Please enter your First Name'})
    last_name = forms.CharField(initial='',label='Last Name',max_length=50,widget=forms.TextInput(attrs={'size':'25'}),error_messages={'required': 'Please enter your Last Name'})
    password1 = forms.CharField(label='Password',max_length=50,widget=forms.PasswordInput(attrs={'size':'25'}),error_messages={'required': 'Please enter your password'})
    password2 = forms.CharField(label='Password (Re-type)',max_length=50,widget=forms.PasswordInput(attrs={'size':'25'}),error_messages={'required': 'Please enter your password'})
    email =     forms.EmailField(initial='',max_length=50,widget=forms.TextInput(attrs={'size':'25'}),error_messages={'required': 'Please enter a valid email address'})
    phone_number = USPhoneNumberField(initial='',label='Phone Number (main)', widget=forms.TextInput(attrs={'size':'25'}),error_messages={'required': 'Please enter your Phone Number'}),


    def clean_username(self):
        data = self.cleaned_data['username']

        #check inputed data for current record in DB
        exist_check=User.objects.filter(username = data).count()

        if exist_check>0:
            raise forms.ValidationError("Username already exists. Please enter another username")

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data

    def clean(self):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if not password1:
            msg = u"You must enter a password"
            self._errors["password1"] = ErrorList([msg])
            self._errors["password2"] = ErrorList([msg])
            return cleaned_data

        if len(password1) < 7:
            msg = u"Your passwords must be at least 8 characters long"
            self._errors["password1"] = ErrorList([msg])
            self._errors["password2"] = ErrorList([msg])
            return cleaned_data

        #define error if user type is agent and entity not set
        if (password1 != password2):
            msg = u"Your passwords do not match. Please re-type your passwords"
            self._errors["password1"] = ErrorList([msg])
            self._errors["password2"] = ErrorList([msg])


        pin = cleaned_data.get("videntity_pin")
        phone_number = cleaned_data.get("phone_number")

        user=User.objects.filter(userprofile__phone_number=phone_number)

        if user.count() > 0:
            msg = u"Your phone_number is already registered."
            self._errors["phone_number"] = ErrorList([msg])

        # Always return the full collection of cleaned data.
        return cleaned_data
