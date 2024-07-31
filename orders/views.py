from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, RedirectView

from orders.forms import RecalculateCartForm, UpdateCartOrderForm, ApplyDiscountForm
from orders.mixins import GetCurrentOrderMixin


class CartView(GetCurrentOrderMixin, TemplateView):
    template_name = 'orders/cart.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'order': self.get_object(),
                        'items_relation': self.get_queryset()})

        return context

    def get_queryset(self):
        # return self.get_object().items.through.objects \
        #     .select_related('item')\
        #     .annotate(full_price=F('item__price') * F('quantity'))
        return self.get_object().get_items_through()


class UpdateCartView(GetCurrentOrderMixin, RedirectView):

    def post(self, request, *args, **kwargs):
        form = UpdateCartOrderForm(request.POST, instance=self.get_object())
        if form.is_valid():
            if kwargs['action'] == 'remove':
                messages.warning(request,
                                 message='Item was deleted from your cart!')

            elif kwargs['action'] == 'clear':
                messages.success(request, message='Your cart was cleared!')
            elif kwargs['action'] == 'pay':
                messages.success(request, message='Success')
            else:
                messages.success(request, message='Item was add to your cart!')
            form.save(kwargs.get('action'))
        else:
            messages.error(request, 'Invalid form data.')
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


class ConfirmCartView(GetCurrentOrderMixin, TemplateView):
    template_name = 'orders/cart_confirm.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'order': self.get_object(),
                        'items_relation': self.get_queryset()})

        return context

    def get_queryset(self):
        return self.get_object().get_items_through()


class SuccessConfirmCartView(TemplateView):
    template_name = 'orders/cart_confirm_success.html'
