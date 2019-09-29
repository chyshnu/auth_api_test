from django.urls import path
from . import views

app_name = 'util'
urlpatterns = [
    path('test_util/', views.test_util, name='test_util'),
]