from django.urls import path

from . import views


app_name = 'authentication'
urlpatterns = [
    path('login', views.CustomLoginView.as_view(), name='login'),
    path('profile', views.UserProfileView.as_view(), name='profile'),
    path('logout', views.CustomLogoutView.as_view(), name='logout'),
    path('registration', views.UserRegistrationFormView.as_view(), name='registration'),
    path('activation/<slug:uidb64>/<slug:token>', views.UserActivationView.as_view(), name='activation'),
    path('password_reset', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<slug:uidb64>/<slug:token>', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete', views.CustomPassworwResetCompleteView.as_view(), name='password_reset_complete'),
]