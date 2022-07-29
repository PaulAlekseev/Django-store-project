from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import get_object_or_404, resolve_url, redirect
from django.http import HttpResponse
from django.views import generic

from .tokens import account_activation_token
from .forms import RegistrationForm
from store.models import Category, Product
from .models import CustomUser, Review


class CustomLoginView(LoginView):

    template_name = 'authentication/user/login.html'
    redirect_authenticated_user = True
    next_page = 'authentication:profile'


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'store:index'
    

class UserRegistrationFormView(generic.edit.FormView):
    template_name = 'authentication/user/registration.html'
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


class UserActivationView(generic.base.View):
    
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
    template_name = 'authentication/user/profile.html'
    model = Category


class CustomPasswordResetView(PasswordResetView):
    template_name = 'authentication/user/password_reset_form.html'
    email_template_name = "authentication/user/password_reset_email.html"
    success_url = reverse_lazy('authentication:password_reset_done')
    

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'authentication/user/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'authentication/user/password_reset_confirm.html'
    success_url = reverse_lazy('authentication:password_reset_complete')


class CustomPassworwResetCompleteView(PasswordResetCompleteView):
    template_name = 'authentication/user/password_reset_complete.html'


class ReviewCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Review
    fields = ['review_pros', 'review_cons', 'review_commentary', 'rating']
    template_name = 'authentication/reviews/add_review.html'

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        product_reviews = product.review_set.all()
        users_already_reviewed = CustomUser.objects.filter(review__in=product_reviews)

        if request.user in users_already_reviewed:
            return redirect(product)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        context.update({
            'product': product,
        })
        return context

    def form_valid(self, form):
        review = form.save(commit=False)
        product = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        review.product = product
        review.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        product = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        return product.get_absolute_url()


class UpdateReviewView(generic.edit.UpdateView):
    fields = ['review_pros', 'review_cons', 'review_commentary', 'rating']
    template_name = 'authentication/reviews/update_review.html'

    def get_object(self, queryset=None):
        review = get_object_or_404(Review.objects.filter(
            id=self.kwargs.get('id'), user=self.request.user
            ).select_related('product')
        )
        return review

    def get_success_url(self):
        product = self.get_object().product
        return product.get_absolute_url()


class DeleteReviewView(generic.edit.DeleteView):
    template_name = 'authentication/reviews/delete_review.html'

    def get_object(self):
        review = get_object_or_404(Review.objects.filter(
            id=self.kwargs.get('id'), user=self.request.user
            ).select_related('product')
        )
        return review

    def get_success_url(self):
        product = self.get_object().product
        return product.get_absolute_url()