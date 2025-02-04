from orders.models import Order


class GetCurrentOrderMixin:

    def get_object(self):
        return Order.objects.get_or_create(
            is_active=True,
            is_paid=False,
            user=self.request.user
        )[0]
