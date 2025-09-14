from multiprocessing.sharedctypes import Value
from unicodedata import name
from django.urls import path
from . import views
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_request, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('home/', views.home, name='home'),
    path('settings/', views.settings, name='settings'),
    path('contact/', views.contact, name='contact'),
    path('mission/', views.mission, name='mission'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)