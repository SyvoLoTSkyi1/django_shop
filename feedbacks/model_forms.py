from django import forms
from feedbacks.models import Feedback


class FeedbackModelForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('user', 'text', 'rating')
