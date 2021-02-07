from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from markdownx.utils import markdownify


from .forms import NoteForm, SignUpForm
from .utils.helpers import queryset_ext, text_splitter, tag_extractor
from .models import Note
from taggit.models import Tag
# Create your views here.


def note_and_tag_list(request, tag):
  username = request.user
  notes_list = Note.objects.filter(user__username=username)
  tags_list = []
  for note in notes_list:
    if not note.trashed:
      note_tags = list(note.tags.all())
      note.note_tags = note.tags.all()
      for tg in note_tags:
        if tg not in tags_list:
          tags_list.append(tg)
  if tag == 'all' or tag == 'search_res':
    notes_list = notes_list.filter(trashed=False)
  elif tag == 'trash':
    notes_list = notes_list.filter(trashed=True)
  else:
    notes_list = notes_list.filter(trashed=False).filter(tags__name=tag)
  return (notes_list, tags_list)

@login_required
def get_user_notes(request, tag='all'):
  notes_list = []
  tags_list = []
  notes_list, tags_list = note_and_tag_list(request, tag)
  #print('note tags are: ', notes_list)

  for note in notes_list:
    note.nt_tags = note.tags.all()
    note.summary = text_splitter(note.note_body, 15)

  template = loader.get_template('notes/user_notes.html')
  context = {
    'notes_list': notes_list,
    'tags_list': tags_list,
    'tag_name': tag,
  }
  return HttpResponse(template.render(context, request))

@login_required
def user_notes_with_note_detail(request, tag, pk):
  notes_list = []
  tags_list = []
  notes_list, tags_list = note_and_tag_list(request, tag)

  for note in notes_list:
    note.nt_tags = note.tags.all()
    note.summary = text_splitter(note.note_body, 15)

  note_number = pk
  note_presented = markdownify(notes_list.get(id=pk).note_body)
  note_tags = notes_list.get(id=pk).tags.names()
  template = loader.get_template('notes/user_notes.html')
  context = {
    'notes_list': notes_list,
    'tags_list': tags_list,
    'tag_name': tag,
    'note_number': note_number,
    'note_presented': note_presented,
    'note_tags': note_tags,
  }
  return HttpResponse(template.render(context, request))

@login_required
def get_search_results(request):
  if request.method == 'POST':
    tag = request.headers['Referer']
    tag = tag_extractor(tag)
    notes_list = []
    tags_list = []

    if tag != 'search_res':
      request.session['tag'] = tag
    else:
      tag = request.session['tag']
    notes_list, tags_list = note_and_tag_list(request, tag)
    
    

    print('=========')
    print('tag is:', tag)
    search_str = request.POST['search-bar']
    #notes_list = notes_list.filter(tags__name=tag)
    print('search string is: ', search_str)
    if len(notes_list) != 0:
      print('success')
    else:
      print('failure')

    notes_list = notes_list.filter(
      Q(note_title__contains=search_str) | Q(note_body__contains=search_str)
    )

    if len(notes_list) != 0:
      search_result_info = 'success'
    else:
      search_result_info = 'failure'
    print('info: ', search_result_info)
    for note in notes_list:
      note.nt_tags = note.tags.all()
      note.summary = text_splitter(note.note_body, 15)
    template = loader.get_template('notes/user_notes.html')
    context = {
      'notes_list': notes_list,
      'tags_list': tags_list,
      'tag_name': 'search_res',
      'search_str': search_str,
      'search_result_info': search_result_info
    }
    return HttpResponse(template.render(context, request))

@login_required
def get_search_results_with_note_detail(request, search_str, pk):
  notes_list = []
  tags_list = []
  #search_tag = 'search_res'
  tag = request.session['tag']
  notes_list, tags_list = note_and_tag_list(request, tag)

  
  notes_list = notes_list.filter(
      Q(note_title__contains=search_str) | Q(note_body__contains=search_str)
    )

  for note in notes_list:
    note.nt_tags = note.tags.all()
    note.summary = text_splitter(note.note_body, 15)

  note_number = pk
  note_presented = markdownify(notes_list.get(id=pk).note_body)
  note_tags = notes_list.get(id=pk).tags.names()
  template = loader.get_template('notes/user_notes.html')
  context = {
    'notes_list': notes_list,
    'tags_list': tags_list,
    'tag_name': 'search_res',
    'note_number': note_number,
    'note_presented': note_presented,
    'note_tags': note_tags,
    'search_str': search_str
  }
  return HttpResponse(template.render(context, request))


class AdminLogin(LoginView):
  template_name = 'notes/login_form.html'


class AdminLogout(LogoutView):
  pass


def signup(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      pw = form.cleaned_data.get('password1')
      user = authenticate(username=username, password=pw)
      login(request, user)
      return redirect('notes:home')
  else:
    form = SignUpForm()
  return render(request, 'notes/signup_form.html', {'form': form})


def home(request):
  user = request.user
  template = loader.get_template('notes/home.html')
  context = {
    'user': user,
  }
  return HttpResponse(template.render(context, request))

@login_required
def new_note(request):
  if request.method == 'POST':
    form = NoteForm(request.POST)
    if form.is_valid():
      newpost = form.save(commit=False)
      newpost.user = request.user
      messages.success(request, 'Note created successfully')
      #newpost.slug = slugify(newpost.title)
      newpost.save()
      # Without this next line the tags won't be saved.
      form.save_m2m()
      return redirect('notes:default_user_prof')
  else:
    form = NoteForm()

  context = {
    'form': form,
  }
  return render(request, 'notes/note_create_form.html', context)

@login_required
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
      messages.success(request, 'Note updated successfully')
      return redirect('notes:default_user_prof')
    else:
      return HttpResponse(form.errors)
  else:
    form = NoteForm(i_data)

  context = {
    'form': form,
  }
  return render(request, 'notes/note_update_form.html', context)

@login_required
def trash_note(request, pk):
  note_obj = Note.objects.get(pk=pk)
  try:
    note_obj.trashed = True
    note_obj.save()
    messages.success(request, 'Note moved to bin successfully')
  except:
    messages.error(request, 'Note could not send to bin')
    
  return redirect('notes:default_user_prof')

@login_required
def untrash_note(request, pk):
  note_obj = Note.objects.get(pk=pk)
  try:
    note_obj.trashed = False
    note_obj.save()
    messages.success(request, 'Note retrieved from bin successfully')
  except:
    messages.error(request, 'Note could not retrieve from bin')
    
  return redirect('/profile/notes/trash/')

@login_required
def delete_note(request, pk):
  note_obj = Note.objects.get(pk=pk)
  try:
    note_obj.delete()
    messages.success(request, 'Note deleted successfully')
  except:
    messages.error(request, 'Note could not deleted')
    
  return redirect('/profile/notes/trash/')