from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv

from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView
from django_filters.views import FilterView

from items.filters import ItemFilter, PopularItemFilter
from items.forms import ImportForm
from items.models import Item, PopularItem
from shop.mixins.views_mixins import StaffUserCheck
from wishlist.models import WishlistItem


class ItemsView(FilterView):
    model = Item
    paginate_by = 6
    filterset_class = ItemFilter
    template_name_suffix = '_list'

    def get_queryset(self):
        qs = self.model.get_items()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'items': self.get_queryset()})
        if self.request.user.is_authenticated:
            wishlist_items = WishlistItem.objects \
                .filter(user=self.request.user) \
                .values_list('item_id', flat=True)
        else:
            wishlist_items = []
        context.update({
            'wishlist_items': wishlist_items,
            'query_params': self.get_query_params()})
        return context

    def get_query_params(self):
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        return query_params.urlencode()


class ItemDetail(DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()

        similar_items = Item.objects.filter(
            category=item.category).exclude(id=item.id)[:3]
        if self.request.user.is_authenticated:
            wishlist_items = WishlistItem.objects.filter(
                user=self.request.user
                ).values_list('item_id', flat=True)
        else:
            wishlist_items = []
        context.update({
            'wishlist_items': wishlist_items,
            'similar_items': similar_items
        })

        return context


@login_required
def export_csv(request, *args, **kwargs):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="items.csv"'},
    )

    fieldnames = ['name', 'description', 'price', 'sku', 'category', 'image']
    writer = csv.DictWriter(response, fieldnames=fieldnames)
    for item in Item.objects.iterator():
        writer.writerow(
            {
                'name': item.name,
                'description': item.description,
                'price': item.price,
                'sku': item.sku,
                'category': item.category,
                'image': settings.DOMAIN + item.image.url,
            }
        )

    return response


class ImportCSVIntoItems(StaffUserCheck, FormView):
    template_name = 'items/import_csv.html'
    form_class = ImportForm
    success_url = reverse_lazy('items')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ItemSearchView(FilterView):
    model = Item
    template_name = 'items/item_list.html'
    filterset_class = ItemFilter
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return Item.objects.filter(name__icontains=query)
        return Item.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        context['query_params'] = self.get_query_params()
        return context

    def get_query_params(self):
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        return query_params.urlencode()


class PopularItemsView(ItemsView):
    model = PopularItem
    template_name = 'items/popular_items.html'
    filterset_class = PopularItemFilter
    paginate_by = 6

    def get_queryset(self):
        return PopularItem.objects.all()
