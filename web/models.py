from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

POSTCHOICE = (
  ('have', 'Offer'),
  ('need', 'Request')
)
PRIORITYCHOICE = (
  ('immediate', 'Immediate / Life-Saving'),
  ('midterm', 'Mid-Term / Life-Sustaining')
)

class Category(models.Model):
  name  = models.CharField(max_length=200)

  def __unicode__(self):
    return self.name

class UserProfile(models.Model):
  user 	= models.ForeignKey(User, unique=True)
  phone = models.CharField(max_length=100)

  def __unicode__(self):
    return self.user

class Post(models.Model):
  created_at  = models.DateTimeField(default=datetime.utcnow)
  title       = models.CharField(max_length=200)
  type        = models.CharField(max_length=10, choices=POSTCHOICE)
  priority    = models.CharField(max_length=10, choices=PRIORITYCHOICE)
  location    = models.CharField(max_length=100)
  geostamp    = models.CharField(max_length=100, blank=True)
  time_start  = models.DateTimeField(default=datetime.utcnow, blank=True)
  time_end    = models.DateTimeField(blank=True)
  category    = models.ForeignKey(Category)
  contact     = models.ForeignKey(User, blank=True, null=True)
  content     = models.TextField()

  def __unicode__(self):
    return self.title

