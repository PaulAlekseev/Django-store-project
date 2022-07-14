from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from store.models import Category


class CustomLoginView(LoginView):

    template_name = 'authentication/login.html'
    redirect_authenticated_user = True
    next_page = 'authentication:profile'


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'store:index'
    

class UserProfileView(generic.list.ListView, LoginRequiredMixin):
    template_name = 'authentication/profile.html'
    model = Category
