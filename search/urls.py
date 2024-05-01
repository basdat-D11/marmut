from django.urls import path
from search.views import *

app_name = 'search'

urlpatterns = [
    path('', search_bar, name='search_bar'),
    path('results/', search_results, name='search_results'),
]