from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from items.models import Item, PopularItem, Category
from main.forms import ContactForm
from main.tasks import send_contact_form
from wishlist.models import WishlistItem


class MainView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()[:3]
        items = Item.objects.all()[:3]
        popular_items = PopularItem.objects.all()[:3]
        if self.request.user.is_authenticated:
            wishlist_items = WishlistItem.objects \
                .filter(user=self.request.user). \
                values_list('item_id', flat=True)
        else:
            wishlist_items = []

        context.update({
            'items': items,
            'popular_items': popular_items,
            'categories': categories,
            'wishlist_items': wishlist_items,

        })

        return context


class ContactView(FormView):
    template_name = 'main/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts')

    def form_valid(self, form):
        send_contact_form(form.cleaned_data['email'],
                          form.cleaned_data['text'])
        messages.success(self.request, "Email has been sent.")
        return super().form_valid(form)
