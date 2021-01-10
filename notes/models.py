from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from markdownx.models import MarkdownxField
from taggit.managers import TaggableManager
# Create your models here.

class User(AbstractUser):
  pass 

class Note(models.Model):
  note_title = models.CharField(max_length=200)
  note_body = MarkdownxField()
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
  )
  trashed = models.BooleanField(default=False)
  published = models.DateField(auto_now_add=True)
  tags = TaggableManager()

  def get_absolute_url(self):
    return reverse('notes:note_detail', kwargs={'pk': self.pk})

  def __str__(self):
    return self.note_title
