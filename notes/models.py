from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class User(AbstractUser):
  pass 

class Note(models.Model):
  note_title = models.CharField(max_length=200)
  note_body = models.TextField()
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
  )

  def __str__(self):
    return self.note_body

class Tag(models.Model):
  tag_name = models.CharField(max_length=150)
  users = models.ManyToManyField(settings.AUTH_USER_MODEL)
  notess = models.ManyToManyField(Note)

  def __str__(self):
    return self.tag_name