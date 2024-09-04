from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.generic import FormView, RedirectView, DetailView, UpdateView

from orders.models import Order
from users.forms import CustomAuthenticationForm
from users.model_forms import SignUpModelForm, SignUpConfirmPhoneForm

User = get_user_model()


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back {form.get_user().email or form.get_user().phone}')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error login')
        return super().form_invalid(form)

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

    def form_valid(self, form):
        user = form.save()
        self.request.session['user_id'] = user.id
        messages.success(self.request, f'User {user.email or user.phone} was created')
        if user.email:
            self.success_url = reverse_lazy('sign_up_activation_email')
        elif user.phone:
            self.success_url = reverse_lazy('sign_up_confirm_phone')

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


class SignUpConfirmEmailView(RedirectView):
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


class SignUpConfirmPhoneView(FormView):
    form_class = SignUpConfirmPhoneForm
    template_name = 'registration/sign_up_confirm_phone.html'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        form = self.get_form()
        if form.is_valid(session_user_id=user_id):
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save(self.request.session['user_id'])
        messages.success(self.request, message='Your account was activated,'
                                               ' you can sign in!')
        return super(SignUpConfirmPhoneView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, message='Please, write valid code!')
        return super(SignUpConfirmPhoneView, self).form_invalid(form)


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_profile.html'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        orders = Order.objects.filter(user=user)
        context['order_count'] = orders.count()
        context['has_active_order'] = orders.filter(is_active=True).exists()

        return context


# class UserUpdateView(LoginRequiredMixin, UpdateView):
#     model = User
#     form_class = UserUpdateForm
#     template_name = 'profile/user_update.html'
#     success_url = reverse_lazy('user_profile')  # URL на який користувач перенаправляється після успішного редагування
#
#     def get_object(self):
#         # Повертаємо поточного користувача
#         return self.request.user