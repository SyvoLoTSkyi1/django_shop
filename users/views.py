from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.generic import FormView, RedirectView

from users.forms import CustomAuthenticationForm
from users.model_forms import SignUpModelForm


User = get_user_model()


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


class SignUpConfirmView(RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        user = self.get_user(kwargs['uidb64'])

        if user is not None:
            token = kwargs['token']

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save(update_fields=('is_active',))
                messages.success(request, 'Confirmation success')
            else:
                messages.error(request, 'Confirmation error')
        return super().get(request, *args, **kwargs)

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()

            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist,
                ValidationError):
            user = None
        return user
