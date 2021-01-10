from django.urls import path
from django.conf import settings


from . import views

app_name = 'notes'

urlpatterns = [
  path('profile/notes/all/', views.get_user_profile, name='default_user_prof'),
  #path('profile/notes/trash/', views.get_user_profile, name='user_prof_trash'),
  path('profile/notes/<tag>/', views.get_user_profile, name='user_prof'),
  path('profile/notes/<tag>/<int:pk>', views.user_profile_with_note_detail, name='user_prof'),
  path('login/', views.AdminLogin.as_view(), name='login'),
  path('', views.home, name='home'),
  path('logout/', views.AdminLogout.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
  path('add-note/', views.new_note, name='note_create'),
  path('update-note/<int:pk>', views.update_note, name='note_update'),
  path('trash/<int:pk>', views.trash_note, name='trash_note'),
  path('untrash/<int:pk>', views.untrash_note, name='untrash_note'),
  path('delete/<int:pk>', views.delete_note, name='delete_note'),
]