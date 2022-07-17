from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import resolve_url, redirect
from django.http import HttpResponse
from django.views import generic

from .tokens import account_activation_token
from .forms import RegistrationForm
from store.models import Category
from .models import CustomUser


class CustomLoginView(LoginView):

    template_name = 'authentication/login.html'
    redirect_authenticated_user = True
    next_page = 'authentication:profile'


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'store:index'
    

class RegistrationFormView(generic.edit.FormView):
    template_name = 'authentication/registration.html'
    form_class = RegistrationForm
    success_url = 'store:index'

    def form_valid(self, form):
        form = self.get_form()
        user = form.save()
        current_site = get_current_site(self.request)
        subject = 'Activate your Account'
        message = render_to_string('authentication/user_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject=subject, message=message)
        return super().form_valid(form)
            
    def get_success_url(self):
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return resolve_url(str(self.success_url))


class ActivationView(generic.base.View):
    
    def get(self, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(self.kwargs.get('uidb64')))
            user = CustomUser.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, user.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, self.kwargs.get('token')):
            user.is_active = True
            user.save()
            login(self.request, user)
            return redirect('authentication:profile')
        else:
            return HttpResponse('2')
        

class UserProfileView(generic.list.ListView, LoginRequiredMixin):
    template_name = 'authentication/profile.html'
    model = Category
