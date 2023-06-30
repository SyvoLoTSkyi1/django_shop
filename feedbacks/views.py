from django.shortcuts import render

from feedbacks.model_forms import FeedbackModelForm
from feedbacks.models import Feedback


def feedbacks(request, *args, **kwargs):

    if request.method == 'POST':
        form = FeedbackModelForm(request.POST)
        if form.is_valid():
            new_feedback = form.save(commit=False)
            new_feedback.text = check_text(form.cleaned_data.get("text"))
            new_feedback.save()
    else:
        form = FeedbackModelForm()
    context = {
        'feedbacks': Feedback.objects.all(),
        'form': form
    }
    return render(request, 'feedbacks/index.html', context=context)


def check_text(text):

    clear_text = ''
    for i in text:
        if i.isalnum() or i == ' ':
            clear_text += i

    return clear_text
