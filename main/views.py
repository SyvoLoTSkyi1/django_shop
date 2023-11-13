from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from main.forms import ContactForm
from main.tasks import send_contact_form


class MainView(TemplateView):
    template_name = 'main/index.html'


class ContactView(FormView):
    template_name = 'main/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts')

    def form_valid(self, form):
        send_contact_form.delay(form.cleaned_data['email'],
                                form.cleaned_data['text'])
        messages.success(self.request, "Email has been sent.")
        return super().form_valid(form)
