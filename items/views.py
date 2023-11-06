from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv

from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView

from items.forms import ImportForm
from items.models import Item
from shop.mixins.views_mixins import StaffUserCheck


class ItemsView(ListView):
    model = Item
    paginate_by = 2

    def get_queryset(self):
        return self.model.get_items()


class ItemDetail(DetailView):
    model = Item


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
