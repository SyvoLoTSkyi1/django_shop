from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from shop.settings import AUTHENTICATION_BACKENDS
from users.forms import CustomAuthenticationForm
from users.model_forms import SignUpModelForm


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = CustomAuthenticationForm
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back {form.get_user().email}')
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error login')
        return super(LoginView, self).form_invalid(form)

    # def get_context_data(self, request, *args, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update({'form': kwargs.get('form') or LoginForm}) # noqa
    #     return context
    #
    # def post(self, request, *args, **kwargs):
    #     context = self.get_context_data(**kwargs)
    #     form = context['form']
    #     form = form(request.POST)
    #     if form.is_valid():
    #         login(request, form.user)
    #     return self.get(request, form=form, *args, **kwargs)


class SignUpView(FormView):
    template_name = 'registration/sign_up.html'
    form_class = SignUpModelForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f'User {user.email} was created')
        login(self.request, user, backend=AUTHENTICATION_BACKENDS[0])
        return super(SignUpView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Sign Up error')
        return super(SignUpView, self).form_invalid(form)

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update({'form': kwargs.get('form') or SignUpModelForm})
    #     return context
    #
    # def post(self, request, *args, **kwargs):
    #     context = self.get_context_data(**kwargs)
    #     form = context['form']
    #     form = form(request.POST)
    #     if form.is_valid():
    #         new_user = form.save()
    #         login(request, new_user)
    #     return self.get(request, form=form, *args, **kwargs)
