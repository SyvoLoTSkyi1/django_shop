from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, RedirectView, UpdateView

from orders.forms import RecalculateCartForm, \
    UpdateCartOrderForm, ApplyDiscountForm
from orders.mixins import GetCurrentOrderMixin
from orders.models import Order
from users.model_forms import UserProfileForm


class CartView(GetCurrentOrderMixin, TemplateView):
    template_name = 'orders/cart.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'order': self.get_object(),
            'items_relation': self.get_queryset()})

        return context

    def get_queryset(self):
        # return self.get_object().items.through.objects \
        #     .select_related('item')\
        #     .annotate(full_price=F('item__price') * F('quantity'))
        return self.get_object().get_items_through()


class UpdateCartView(GetCurrentOrderMixin, RedirectView):

    def post(self, request, *args, **kwargs):
        action = kwargs.get('action')
        form = UpdateCartOrderForm(request.POST,
                                   instance=self.get_object(),
                                   action=action)

        if form.is_valid():
            try:
                form.save(kwargs.get('action'))
                if kwargs['action'] == 'remove':
                    messages.warning(request,
                                    message='Item was deleted from your cart!')

                elif kwargs['action'] == 'clear':
                    messages.success(request, message='Your cart was cleared!')
                elif kwargs['action'] == 'pay':
                    messages.success(request, message='Success')
                else:
                    messages.success(request, message='Item was add to your cart!')
            except ValidationError as e:
                messages.error(request, e.message)

        else:
            error_message = ' '.join([str(error) for error in form.non_field_errors()])
            messages.error(request, error_message)
        return self.get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if kwargs['action'] == 'remove':
            return reverse_lazy('cart')
        elif kwargs['action'] in ('add', 'clear',):
            return reverse_lazy('items')
        elif kwargs['action'] == 'pay':
            return reverse_lazy('success_confirm_cart')


class RecalculateCartView(GetCurrentOrderMixin, RedirectView):
    url = reverse_lazy('cart')

    def post(self, request, *args, **kwargs):
        form = RecalculateCartForm(request.POST, instance=self.get_object())
        if form.is_valid():
            messages.success(request, message='Your cart was recalculated!')
            form.save()
        return self.get(request, *args, **kwargs)


class ApplyDiscountView(GetCurrentOrderMixin, RedirectView):
    url = reverse_lazy('confirm_cart')

    def post(self, request, *args, **kwargs):
        form = ApplyDiscountForm(request.POST, order=self.get_object())
        if form.is_valid():
            form.apply()
        return self.get(request, *args, **kwargs)


# class ConfirmCartView(GetCurrentOrderMixin, TemplateView):
#     template_name = 'orders/cart_confirm.html'
#
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({'order': self.get_object(),
#                         'items_relation': self.get_queryset()})
#
#         return context
#
#     def get_queryset(self):
#         return self.get_object().get_items_through()


class ConfirmCartView(UpdateView):
    template_name = 'orders/cart_confirm.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('confirm_cart')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """
        Return current user for form.
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        """
        Add Order to form.
        """
        context = super().get_context_data(**kwargs)
        order = Order.objects.filter(user=self.get_object(), is_active=True)[0]
        context.update({
            'order': order,
            'items_relation': order.get_items_through()})
        return context

    def get_form_kwargs(self):
        """
        Send User to form.
        """
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'instance': self.get_object(),
            'require_fields': True
        })
        return kwargs

    def form_valid(self, form):
        """
        Check the form and save it.
        """
        form.save()
        messages.success(self.request, 'Your details have been updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        If form is invalid, show message with errors
        """
        messages.error(self.request, 'Error updating your details. Please check the form.')
        return super().form_invalid(form)


class SuccessConfirmCartView(TemplateView):
    template_name = 'orders/cart_confirm_success.html'
