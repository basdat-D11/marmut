from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('tes', home, name='home'),
    path('page_login', page_login, name='page_login'),
    path('dashboard', login, name='dashboard'),
    path('validate_login' , validate_login, name='validate_login'),\
    path('register', register, name='register'),
]