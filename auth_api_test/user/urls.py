from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('test_json', views.json_response_test),
    path('login', views.login),
    path('send_vcode', views.send_vcode),
    path('mobile_login', views.mobile_login),
]

