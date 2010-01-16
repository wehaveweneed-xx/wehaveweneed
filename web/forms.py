#!/usr/bin/env python
from django import forms
from wehaveweneed.web.models import Posy
#from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django.contrib.localflavor.us.forms import *

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title', 'type', 'priority', 
                  'location', 'geostamp',
                  'time_start',
                  'time_end',
                  'category',
                  'content',)