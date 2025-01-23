from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.generic import FormView, RedirectView, \
    DetailView, UpdateView, ListView

from orders.models import Order
from users.forms import CustomAuthenticationForm
from users.model_forms import SignUpModelForm, \
    ConfirmPhoneForm, UserProfileForm
from users.tasks import send_confirmation_email, \
    send_verification_sms

User = get_user_model()


class CustomLoginView(LoginView):
    template_name = 'users/registration/login.html'
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        messages.success(self.request,
                         f'Welcome back {form.get_user().email or form.get_user().phone}')  # noqa
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error login')
        return super().form_invalid(form)


class SignUpView(FormView):
    template_name = 'users/registration/sign_up.html'
    form_class = SignUpModelForm

    def form_valid(self, form):
        user = form.save()
        self.request.session['user_id'] = user.id
        messages.success(self.request,
                         f'User {user.email or user.phone} was created')  # noqa

        if user.email:
            self.success_url = reverse_lazy('activation_email')
        elif user.phone:
            self.success_url = reverse_lazy('confirm_phone')

        return super(SignUpView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Sign Up error')
        return super(SignUpView, self).form_invalid(form)


class ConfirmEmailView(RedirectView):

    def get(self, request, *args, **kwargs):
        user = self.get_user(kwargs['uidb64'])

        if user is not None:
            token = kwargs['token']

            if default_token_generator.check_token(user, token):
                if not user.is_active:
                    user.is_active = True
                user.is_email_valid = True
                user.save(update_fields=('is_active', 'is_email_valid',))
                messages.success(request, 'Your email successfully confirmed!')
            else:
                messages.error(request, 'Confirmation error')

        self.url = reverse_lazy('user_profile') \
            if user.last_login else reverse_lazy('login')

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


class ConfirmPhoneView(FormView):
    form_class = ConfirmPhoneForm
    template_name = 'users/registration/confirm_phone.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        user_id = self.request.session.get('user_id') if \
            self.request.user.is_anonymous else \
            self.request.user.id
        form = self.get_form()
        if form.is_valid(user_id=user_id):
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        user_id = self.request.session.get('user_id') if \
            self.request.user.is_anonymous else \
            self.request.user.id
        user = form.save(user_id)
        messages.success(self.request,
                         message='Your phone successfully confirmed!')

        self.success_url = reverse_lazy('user_profile') if \
            user.last_login else \
            reverse_lazy('login')
        return super(ConfirmPhoneView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, message='Code error!')
        return super(ConfirmPhoneView, self).form_invalid(form)


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


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/user_profile_update.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request,
                         'Your profile was successfully updated!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the error below.')
        return super().form_invalid(form)


class UserOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'users/user_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_count'] = self.get_queryset().count()
        return context


class UserOrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'users/user_order_detail.html'

    def get_object(self, queryset=None):
        user = self.request.user
        order_id = self.kwargs.get('pk')
        return get_object_or_404(Order, id=order_id, user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'order': self.get_object(),
            'items_relation': self.get_queryset()})

        return context

    def get_queryset(self):
        return self.get_object().get_items_through()


class ConfirmPhoneEmailProfileView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):

        confirmation_type = kwargs.get('type')
        user = self.request.user

        if confirmation_type == 'email':
            return self.confirm_email(user)
        elif confirmation_type == 'phone':
            return self.confirm_phone(user)
        else:
            messages.error(self.request, "Invalid confirmation type.")
            return reverse_lazy('user_profile')

    def confirm_email(self, user):
        if user.email and not user.is_email_valid:
            send_confirmation_email.delay(user)
            messages.success(self.request,
                             "A confirmation was sent to your email.")
            return reverse_lazy('activation_email')
        else:
            messages.error(self.request,
                           "Your email is already verified or not provided.")
            return reverse_lazy('user_profile')

    def confirm_phone(self, user):
        if user.phone and not user.is_phone_valid:
            send_verification_sms.delay(user, user.phone)
            messages.success(self.request,
                             "A confirmation code was sent to your phone.")
            return reverse_lazy('confirm_phone')
        else:
            messages.error(self.request,
                           "Your phone number is already verified or not provided.")  # noqa
            return reverse_lazy('user_profile')
