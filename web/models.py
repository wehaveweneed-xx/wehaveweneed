from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

POSTCHOICE = (
  ('have', 'Have'),
  ('need', 'Need'),
)
PRIORITYCHOICE = (
  ('short', 'Immediate / Life-Saving'),
  ('mid', 'Mid-Term / Life-Sustaining'),
  ('long', 'Long-Term / Life-Enhancing'),
)

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='child')
    
    class Meta:
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    user  = models.ForeignKey(User, unique=True)
    phone = models.CharField(max_length=100)

    def __unicode__(self):
        return 'profile of %s' % self.user.username


class Post(models.Model):
    created_at  = models.DateTimeField(default=datetime.utcnow)
    title       = models.CharField(max_length=200)
    type        = models.CharField(max_length=10, choices=POSTCHOICE)
    priority    = models.CharField(max_length=10, choices=PRIORITYCHOICE)
    location    = models.CharField(max_length=100)
    geostamp    = models.CharField(max_length=100, blank=True)
    time_start  = models.DateTimeField(default=datetime.utcnow, blank=True)
    time_end    = models.DateTimeField(blank=True, null=True)
    category    = models.ForeignKey(Category)
    contact     = models.ForeignKey(User, blank=True, null=True)
    content     = models.TextField()
    responses   = models.IntegerField(default=0)
    fulfilled   = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)

    def __unicode__(self):
        return self.title
