from django import forms
from .models import Note
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignUpForm(UserCreationForm):
  class Meta:
    model = User
    fields = ('username', 'password1', 'password2')

    
class NoteForm(forms.ModelForm):
  class Meta:
    model = Note
    fields = (
      'note_title',
      'note_body',
      'tags',
    )
    labels = {
      'note_title': ('Title'),
      'note_body': ('Note'),
      'tags': ('Tags'),
    }
    widgets = {
      'tags': forms.TextInput(attrs={'data-role': 'tagsinput'}),
    }
    
