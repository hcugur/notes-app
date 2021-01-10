from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from markdownx.utils import markdownify


from .forms import NoteForm
from .utils.helpers import queryset_ext, text_splitter
from .models import Note
from taggit.models import Tag
# Create your views here.

def get_user_profile(request, tag='all'):
  username = request.user
  notes_list = Note.objects.filter(user__username=username)
  tags_list = []

  for note in notes_list:
    if not note.trashed:
      note_tags = list(note.tags.all())
      for tg in note_tags:
        if tg not in tags_list:
          tags_list.append(tg)
  
  if tag == 'all':
    notes_list = notes_list.filter(trashed=False)
  elif tag == 'trash':
    notes_list = notes_list.filter(trashed=True)
  else:
    notes_list = notes_list.filter(trashed=False).filter(tags__name=tag)

  for note in notes_list:
    note.summary = text_splitter(note.note_body, 15)

  template = loader.get_template('notes/user_profile.html')
  context = {
    'notes_list': notes_list,
    'tags_list': tags_list,
    'tag_name': tag,
  }
  return HttpResponse(template.render(context, request))

def user_profile_with_note_detail(request, tag, pk):
  username = request.user
  notes_list = Note.objects.filter(user__username=username)
  tags_list = []
  for note in notes_list:
    if not note.trashed:
      note_tags = list(note.tags.all())
      for tg in note_tags:
        if tg not in tags_list:
          tags_list.append(tg)
  
  if tag == 'all':
    notes_list = notes_list.filter(trashed=False)
  elif tag == 'trash':
    notes_list = notes_list.filter(trashed=True)
  else:
    notes_list = notes_list.filter(trashed=False).filter(tags__name=tag)

  for note in notes_list:
    note.summary = text_splitter(note.note_body, 15)

  note_number = pk
  note_presented = markdownify(notes_list.get(id=pk).note_body)
  note_tags = notes_list.get(id=pk).tags.names()
  print('note tags:', note_tags)
  template = loader.get_template('notes/user_profile.html')
  context = {
    'notes_list': notes_list,
    'tags_list': tags_list,
    'tag_name': tag,
    'note_number': note_number,
    'note_presented': note_presented,
    'note_tags': note_tags,
  }
  return HttpResponse(template.render(context, request))

class AdminLogin(LoginView):
  template_name = 'notes/login_form.html'

class AdminLogout(LogoutView):
  pass


def home(request):
  user = request.user
  template = loader.get_template('notes/home.html')
  context = {
    'user': user,
  }
  return HttpResponse(template.render(context, request))


def new_note(request):
  form = NoteForm(request.POST)
  if form.is_valid():
    newpost = form.save(commit=False)
    newpost.user = request.user
    messages.success(request, 'Form submission successful')
    #newpost.slug = slugify(newpost.title)
    newpost.save()
    # Without this next line the tags won't be saved.
    form.save_m2m()
    return redirect('notes:default_user_prof')

  context = {
    'form': form,
  }
  return render(request, 'notes/note_create_form.html', context)


def update_note(request, pk):
  i_note_obj = Note.objects.get(pk=pk)
  i_note_title = i_note_obj.note_title
  i_note_body = i_note_obj.note_body
  i_note_tags = queryset_ext(i_note_obj.tags.names())
  i_data = {
    'note_title': i_note_title,
    'note_body': i_note_body,
    'tags': i_note_tags
  }
  if request.method == 'POST':
    form = NoteForm(request.POST, instance=i_note_obj)
    if form.is_valid():
      cd = form.cleaned_data
      obj = form.save(commit=False)
      if i_data['note_title'] != cd['note_title']:
        obj.note_title = cd['note_title']
      if i_data['note_body'] != cd['note_body']:
        obj.note_body = cd['note_body']
      obj.tags.set(''.join(cd['tags']))
      #newpost.slug = slugify(newpost.title)
      obj.save()
      # Without this next line the tags won't be saved.
      form.save_m2m()
      messages.success(request, 'Form update successful')
      return redirect('notes:default_user_prof')
    else:
      return HttpResponse(form.errors)
  else:
    form = NoteForm(i_data)

  context = {
    'form': form,
  }
  return render(request, 'notes/note_update_form.html', context)


def trash_note(request, pk):
  note_obj = Note.objects.get(pk=pk)
  try:
    note_obj.trashed = True
    note_obj.save()
    messages.success(request, 'Note moved to bin successfully')
  except:
    messages.error(request, 'Note could not send to bin')
    
  return redirect('notes:default_user_prof')


def untrash_note(request, pk):
  note_obj = Note.objects.get(pk=pk)
  try:
    note_obj.trashed = False
    note_obj.save()
    messages.success(request, 'Note retrieved from bin successfully')
  except:
    messages.error(request, 'Note could not retrieve from bin')
    
  return redirect('/profile/notes/trash/')


def delete_note(request, pk):
  note_obj = Note.objects.get(pk=pk)
  try:
    note_obj.delete()
    messages.success(request, 'Note deleted successfully')
  except:
    messages.error(request, 'Note could not deleted')
    
  return redirect('/profile/notes/trash/')