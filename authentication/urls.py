from django.urls import path

from . import views


app_name = 'authentication'
urlpatterns = [
    path('login', views.CustomLoginView.as_view(), name='login'),
    path('profile', views.UserProfileView.as_view(), name='profile'),
    path('logout', views.CustomLogoutView.as_view(), name='logout'),
    path('registration', views.RegistrationFormView.as_view(), name='registration'),
    path('activation/<slug:uidb64>/<slug:token>/', views.ActivationView.as_view(), name='activation'),
]