from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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
