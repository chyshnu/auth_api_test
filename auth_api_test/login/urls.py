from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
    path('test_json/', views.json_response_test, name='test_json'),
    path('test_session/', views.session_test, name='test_session'),
    path('user_login/', views.user_login, name='user_login'),
]

