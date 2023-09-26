from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from feedbacks.forms import ContactForm
from feedbacks.model_forms import FeedbackModelForm, check_text
from feedbacks.models import Feedback


@login_required
def feedbacks(request, *args, **kwargs):
    user = request.user
    if request.method == 'POST':
        form = FeedbackModelForm(user=user, data=request.POST)
        if form.is_valid():
            new_feedback = form.save(commit=False)
            new_feedback.text = check_text(form.cleaned_data.get("text"))
            messages.success(request, message='Thank you for your feedback!')
            new_feedback.save()
        else:
            messages.warning(request, message='Something went wrong!')

    else:
        form = FeedbackModelForm(user=user)
    context = {
        'feedbacks': Feedback.get_feedbacks(),
        'form': form
    }
    return render(request, 'feedbacks/index.html', context=context)


class ContactView(FormView):
    template_name = 'feedbacks/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts')

    def form_valid(self, form):
        send_contact_form.delay(form.cleaned_data['email'], form.cleaned_data['text'])
        messages.success(self.request, "Email has been sent.")
        return super().form_valid(form)
