from django.urls import path
from . import views


urlpatterns = [
    path('', views.user_login),
    path('/sign_up', views.sign_up),
    path('/login', views.user_login),
    path('/test', views.test),
    path('/check_session_view', views.check_session_view),
    path('/profile_view', views.profile_view),
]