from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
  class Meta:
    model = Note
    fields = (
      'note_title',
      'note_body',
      'tags',
    )
    widgets = {
      'tags': forms.TextInput(attrs={'data-role': 'tagsinput'}),
    }
    