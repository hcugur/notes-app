from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView

from .utils.user_page_view import pages_list

from .models import Note
# Create your views here.

def get_user_profile(request):
  username = request.user
  notes_list = Note.objects.filter(user__username=username)[:6]
  
  template = loader.get_template('notes/user_profile.html')
  
  context = {
    'notes_list': notes_list
  }
  return HttpResponse(template.render(context, request))

class AdminLogin(LoginView):
  template_name = 'notes/login_form.html'

def home(request):
  user = request.user

  template = loader.get_template('notes/home.html')

  context = {
    'user': user,
  }

  return HttpResponse(template.render(context, request))


def user_notes_page(request):
  username = request.user
  notes_list = Note.objects.filter(user__username=username)
  paginator = Paginator(notes_list, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  template = loader.get_template('notes/user_profile.html')
  page_list = pages_list(paginator, page_number)
  context = {
    'notes_list': page_obj,
    'pages': page_list
  }
  return HttpResponse(template.render(context, request))