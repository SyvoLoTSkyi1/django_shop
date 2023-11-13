from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, RedirectView

from orders.forms import RecalculateCartForm, UpdateCartOrderForm
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
        return self.get_object().items.through.objects \
            .select_related('item')\
            .annotate(full_price=F('item__price') * F('quantity'))


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
                messages.success(request, message='Your order was payed')
            else:
                messages.success(request, message='Item was add to your cart!')
            form.save(kwargs.get('action'))
        return self.get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy(
            'cart' if kwargs['action'] == 'remove' else 'items')


class RecalculateCartView(GetCurrentOrderMixin, RedirectView):
    url = reverse_lazy('cart')

    def post(self, request, *args, **kwargs):
        form = RecalculateCartForm(request.POST, instance=self.get_object())
        if form.is_valid():
            messages.success(request, message='Your cart was recalculated!')
            form.save()
        return self.get(request, *args, **kwargs)
