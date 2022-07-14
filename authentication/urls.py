from django.urls import path

from . import views


app_name = 'authentication'
urlpatterns = [
    path('login', views.CustomLoginView.as_view(), name='login'),
    path('profile', views.UserProfileView.as_view(), name='profile'),
    path('logout', views.CustomLogoutView.as_view(), name='logout'),
]